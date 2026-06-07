# ペルソナ生成までの実験実行レポート

作成日: 2026-06-06  
対象config: `configs/experiment.example.yaml`  
対象データ: Inside Airbnb Tokyo snapshot `data/raw/inside_airbnb/tokyo/2025-09-29`  
目的: Airbnbレビューだけを用いて、感情疑似ラベル、感情fine-tuned encoder、全レビューembedding、クラスタリング、根拠付きペルソナ生成までを一貫して実行する。

## 1. 実行環境

GPU実行を前提に環境を確認した。

| 項目 | 値 |
|---|---|
| PyTorch | `2.8.0+cu128` |
| CUDA available | `true` |
| CUDA version | `12.8` |
| GPU | `NVIDIA GeForce RTX 3070 Laptop GPU` |
| dependency check | `pip check`: no broken requirements |

本実験ではCUDA対応PyTorchを導入し、fine-tuneと全レビューembeddingをGPUで実行した。

## 2. 実行したパイプライン

実行済みステップ:

```powershell
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli init -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli preprocess-airbnb -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli validate-occupancy -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli label-airbnb-sentiment -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli train -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli evaluate-sentiment-encoder -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli embed -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli cluster -c configs\experiment.example.yaml
.\.venv\Scripts\python.exe -m sentipersona_airbnb.cli personas -c configs\experiment.example.yaml
```

`timeseries` と最終downstream評価は、今回の依頼範囲である「ペルソナ生成まで」には含めていない。

### 2.1 使用モデル一覧

「Qwen34;b」ではなく、正式採用したペルソナ生成モデルは Ollama の `qwen3:4b` である。`qwen3:30b` と `qwen2.5:1.5b` も比較確認したが、全クラスタの正式ペルソナ生成には使っていない。

| 用途 | 採用モデル / 手法 | ローカル配置 / 実行名 | 採用理由 | 備考 |
|---|---|---|---|---|
| 感情疑似ラベル生成 | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` | `models/finetune` | positive/negativeの二値sentimentを高速に付与できる | Airbnb固有モデルではないため high-confidence のみ採用 |
| base embedding encoder | `BAAI/bge-base-en-v1.5` | `models/sentense` | sentence embedding向けで、クラスタリング前提の表現を作りやすい | フォルダ名は `sentense` のまま運用 |
| fine-tuned encoder | BGE baseをAirbnb疑似sentimentでsupervised contrastive fine-tune | `models/senticse/tokyo_senti_persona/` | Airbnbレビューの感情軸をembeddingに反映する | 本番embeddingで採用 |
| 次元圧縮 | UMAP | config内設定 | 高次元embeddingの局所構造を保ちつつHDBSCANへ渡す | 本番では並列化し、visual UMAP別fitは省略 |
| clustering | HDBSCAN | config内設定 | クラスタ数を事前固定せず、noiseを扱える | noise ratioは高め |
| ペルソナ生成 正式採用 | Ollama `qwen3:4b` | `qwen3:4b` | JSON schema modeで安定して構造化出力できた | 5クラスタ x 3回生成で正式採用 |
| ペルソナ生成 比較 | Ollama `qwen3:30b` | `qwen3:30b` | 大きいモデルで日本語化が改善するか確認 | 1クラスタ試行。日本語化は改善せず、正式採用しない |
| ペルソナ生成 比較 | Ollama `qwen2.5:1.5b` | `qwen2.5:1.5b` | 軽量モデルでschema追従できるか確認 | 1クラスタ試行。rank検証で失敗 |

### 2.2 処理時間

実行時間は、コマンド実行ログと成果物更新時刻から整理した。いくつかの工程では途中失敗や最適化の再実行があったため、下表では「成功runの目安」を中心に示す。

| 工程 | 入力規模 | 成功runの所要時間目安 | 備考 |
|---|---:|---:|---|
| `init` | directory setup | 数秒 | `reports/paths.json` 作成 |
| `preprocess-airbnb` | raw reviews 1,004,917件 | 約1分 | clean後、本番対象528,718件を生成 |
| `validate-occupancy` | 8,539 matching rows | 約14秒 | `passed=false` |
| `label-airbnb-sentiment` | train 41,601件 + eval 61,453件 | 約8-13分 | GPU使用。途中のbug fix前後を含む成果物時刻差では約13分 |
| `train` | teacher 3,836件 | 約6分 | `device=cuda`, 5 epochs |
| `evaluate-sentiment-encoder` | balanced sample 2,000件 | 約1分 | baseとfine-tunedを比較 |
| `embed` | 528,718件 | 約84分 | 初回短timeoutを除いた成功run。成果物時刻差では約95分 |
| `cluster` | 528,718 embeddings | 約28分 | 最初はUMAP逐次実行で約4時間timeout。並列化後の成功runが約28分 |
| `personas` | 5 clusters x 12代表レビュー x 3回 | 563秒、約9.4分 | `qwen3:4b` 正式run |
| `pytest` | 16 tests | 約6.5秒 | `16 passed` |
| `ruff` | src + tests | 約0.4秒 | passed |

### 2.3 数値評価指標の読み方

| 指標 | 良い方向 | 目安 | 今回の値 | 解釈 |
|---|---|---|---:|---|
| high-confidence label count | 多いほどよいが、品質とのtrade-off | positive/negative両方が十分にあること | train 3,836 / eval 6,322 | 3か月窓からbalanced teacherを作るには十分 |
| high-confidence score mean | 高いほど疑似ラベルが安定 | `0.95`以上を採用、平均は高いほどよい | train 0.9941 / eval 0.9941 | teacherはかなり高信頼 |
| SgTS delta | 高いほど同じsentimentが近く、異なるsentimentが遠い | baseより大きいことが重要 | 0.0537 -> 0.3934 | fine-tuneで大幅改善 |
| cosine silhouette | 高いほどラベル分離がよい | `-1`から`1`。0付近は弱い、0.5以上は強い分離 | 0.1095 -> 0.7984 | sentiment分離は非常に強く改善 |
| centroid cosine distance | 高いほどpositive/negative中心が離れる | baseより大きいことが重要 | 0.0506 -> 0.3862 | 感情中心の距離が拡大 |
| clustering silhouette | 高いほどクラスタ内が近く、クラスタ間が離れる | `-1`から`1`。0.30以上なら一定のまとまり | 0.3126 | 閾値は超えるが強いクラスタとは言い切れない |
| Davies-Bouldin | 低いほどクラスタがよい | 0に近いほどよい。1前後は中程度 | 0.9699 | 悪くはないが改善余地あり |
| noise ratio | 低いほど多くの点がクラスタに入る | 本設定では0.20以下を目安 | 0.3949 | 高い。曖昧レビュー除外か、クラスタ粒度不適合の可能性 |
| coverage ratio | 高いほどpersona生成が全クラスタを覆う | 1.0が理想 | 1.0 | 全クラスタ生成成功 |
| total failures | 低いほどよい | 0が理想 | 0 | JSON生成・validationとも成功 |
| name consistency | 高いほど反復生成が安定 | 1.0が理想、設定閾値以上でpassed | mean 1.0 / min 1.0 | 3回生成すべて同じpersona名 |
| recurring expression count mean | 1-5の範囲で、十分な根拠表現が出るほどよい | 最大5。ただし無理な水増しは悪い | 5.0 | 各クラスタで5件出力。根拠確認が重要 |
| confidence_counts | highが多いほどモデル判断は強い | high偏りは良いが過信に注意 | high 5 | 代表レビュー上は一貫性が高い |

## 3. データ分割

Kaggleの既存感情データは使わず、Airbnbレビューから疑似ラベルを作成した。

| 用途 | ファイル | 件数 |
|---|---|---:|
| 本番embedding / clustering / persona | `data/processed/airbnb_reviews_clean_all.parquet` | 528,718 |
| fine-tune候補レビュー | `data/processed/airbnb_reviews_finetune_window.parquet` | 41,601 |
| encoder評価候補レビュー | `data/processed/airbnb_reviews_sentiment_eval_window.parquet` | 61,453 |
| high-confidence teacher | `data/interim/teacher_reviews.parquet` | 3,836 |
| high-confidence encoder評価 | `data/interim/sentiment_eval_reviews.parquet` | 6,322 |

fine-tune windowは最新3か月、sentiment encoder評価windowはその直前3か月であり、追加学習と評価の時系列リークを避けている。ペルソナ生成本番では全レビュー528,718件を使用した。

考察:

- 最新3か月のみをfine-tuneに使う設計は、計算量を抑えつつ、直近のレビュー文体と宿泊体験をencoderへ反映する実務的な妥協である。
- 一方で、本番のクラスタリングとペルソナ生成は全レビューを使うため、追加学習データだけにペルソナ発見範囲が閉じない。この分離により、「学習は軽く、本番発見は広く」という実験設計になっている。
- 評価用3か月をfine-tune windowの直前に分けたことで、同じレビューを学習と評価に使うリークは避けられている。ただし、疑似ラベル生成器は同じDistilBERTであるため、評価は人手正解ではなく「疑似ラベルに対する分離性評価」である。

## 4. 感情疑似ラベル生成

使用モデル:

- `models/finetune`
- 元モデル: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- high confidence閾値: `0.95`
- teacher label: `positive=1`, `negative=0`

結果:

| split | 入力件数 | high-confidence件数 | positive | negative | 平均confidence |
|---|---:|---:|---:|---:|---:|
| train | 41,601 | 3,836 | 1,918 | 1,918 | 0.9941 |
| eval | 61,453 | 6,322 | 3,161 | 3,161 | 0.9941 |

positive/negativeはbalanced sampling済みで、fine-tune時のクラス不均衡を抑えた。

考察:

- Airbnbレビューはpositiveに大きく偏るため、raw分布のまま学習するとencoderがpositive中心の空間を作りやすい。balanced samplingは、negative方向の表現を明示的に学習させるために妥当である。
- high-confidence閾値 `0.95` により、疑似ラベルのノイズを減らしている。一方で、曖昧・mixed・皮肉・文脈依存のレビューは落ちやすく、ペルソナ発見に必要なニュアンスが減る可能性がある。
- train/evalとも高信頼データの平均confidenceが約 `0.994` であり、teacherとして使うにはかなり厳選された集合である。ただし、SST-2由来モデルはAirbnb固有の「狭いが快適」「古いが立地が良い」のような複合評価を完全には捉えない可能性がある。

## 5. Sentiment Fine-tune

使用base encoder:

- `models/sentense`
- 元モデル: `BAAI/bge-base-en-v1.5`

fine-tune設定:

| 項目 | 値 |
|---|---|
| loss | supervised contrastive loss |
| epochs | 5 |
| batch size | 32 |
| max length | 256 |
| mixed precision | true |
| device | cuda |
| 出力 | `models/senticse/tokyo_senti_persona/` |

学習ログの最終epochでは、`sgts_delta=0.3558`、`train_loss=2.7749` だった。

考察:

- BGE base encoderは本来semantic embedding向けであり、感情分類専用ではない。supervised contrastive lossでpositive同士、negative同士を近づけることで、レビュー空間に感情軸を追加する狙いは明確である。
- epochごとのSgTS deltaは改善しており、fine-tuneが感情方向の分離を学習していることが確認できる。
- ただし、感情軸を強めすぎると、宿泊目的、設備、立地、清潔さなどのsemantic要素が薄まる危険がある。そのため、この実験ではencoder単体評価だけでなく、後段のクラスタ品質とペルソナ品質もあわせて見る必要がある。

## 6. Sentiment Encoder評価

評価データはfine-tuneに使っていない直前3か月のhigh-confidenceレビューから2,000件をbalanced sampleした。

| 指標 | base encoder | fine-tuned encoder | 改善幅 |
|---|---:|---:|---:|
| SgTS delta | 0.0537 | 0.3934 | +0.3397 |
| cosine silhouette | 0.1095 | 0.7984 | +0.6889 |
| centroid cosine distance | 0.0506 | 0.3862 | +0.3355 |

判定: fine-tuned encoderは、positive/negativeの感情分離を大きく改善した。

考察:

- SgTS delta、cosine silhouette、centroid distanceがすべて大きく改善しており、fine-tuned encoderは疑似感情ラベルに対する分離性能を明確に高めた。
- 特にsilhouetteが `0.1095` から `0.7984` へ上がっている点は、positive/negativeの境界がembedding空間上でかなり明瞭になったことを示す。
- 一方で、この改善は「感情ラベル分離」の改善であり、「ペルソナ発見に最適なsemantic構造」の改善と同義ではない。base encoderとのクラスタ比較や、fine-tune強度のablationは追加実験として価値が高い。

## 7. 全レビューEmbedding

fine-tuned encoderで全レビューをembeddingした。

| 項目 | 値 |
|---|---|
| 入力レビュー | 528,718 |
| embedding shape | `[528718, 768]` |
| dtype | `float32` |
| 出力 | `data/processed/airbnb_review_embeddings.npy` |
| manifest | `reports/embedding_manifest.json` |

考察:

- 追加学習は3か月のみだが、embedding対象は全レビューであるため、ペルソナ生成は最新データだけではなく、Tokyo Airbnbレビュー全体の反復パターンに基づいている。
- GPU環境で全528,718件を処理できたことにより、サンプリングではなく全量embeddingに基づくクラスタリングが可能になった。
- embedding shape `[528718, 768]` は、行数がcleaned production reviewsと一致しており、後段のcluster labelとの対応も保たれている。

## 8. Clustering

UMAP + HDBSCANでレビュークラスタを生成した。

| 指標 | 値 |
|---|---:|
| 入力件数 | 528,718 |
| cluster数 | 5 |
| noise ratio | 0.3949 |
| silhouette | 0.3126 |
| Davies-Bouldin | 0.9699 |
| silhouette sample size | 10,000 |

解釈:

- silhouetteは設定閾値 `0.30` を上回った。
- noise ratioは `0.3949` と高く、設定上の目安 `0.20` より悪い。これはクラスタ外のレビューをかなり厳しくnoise扱いしていることを示す。
- ペルソナ生成ではnoiseを除外し、5クラスタそれぞれから代表レビューを抽出した。

考察:

- silhouetteは閾値を超えており、生成された非noiseクラスタの内部まとまりは一定程度ある。
- noise ratioが高い点は重要な論点である。HDBSCANが曖昧レビューをnoiseとして落としている可能性もあるが、ペルソナ化できるクラスタが5個に絞られ、細かなニッチ嗜好を取り逃がしている可能性もある。
- 研究目的が「安定した大きなペルソナ発見」であれば現在の設定は許容しやすい。一方で「小規模だが重要な不満・特殊ニーズ」を拾うなら、`min_cluster_size_ratio` を下げる、UMAP次元数を変える、base encoderとの比較を行う必要がある。

## 9. ペルソナ生成

使用モデル:

- 正式採用: Ollama `qwen3:4b`
- 比較確認: `qwen3:30b` は日本語化の改善なし、`qwen2.5:1.5b` はschema検証で失敗

モデル比較の詳細:

| モデル | 生成範囲 | 結果 | 所要時間目安 | 採用判断 |
|---|---|---|---:|---|
| `qwen3:4b` | 全5クラスタ、各3回 | 全クラスタでschema validation成功。name consistencyも全クラスタ1.0 | 約9.4分 | 正式採用 |
| `qwen3:30b` | cluster 0のみ試行 | schema validationは成功。ただし `output_language: Japanese` 指定でも英語出力で、4Bとの差が小さい | cluster 0の1回で約132秒 | 全量生成には使わない |
| `qwen2.5:1.5b` | cluster 0のみ試行 | JSONは出たが、`recurring_expressions` のrank順序検証で失敗 | cluster 0の1回で約13秒 | 不採用 |

比較試行の出力例:

| モデル | cluster | persona_name | description / 失敗理由 |
|---|---:|---|---|
| `qwen3:4b` | 0 | `Shinjuku/Shibuya Explorer` | Travelers seeking to explore Tokyo's major districts prioritize walkable access to Shinjuku and Shibuya with responsive hosts. |
| `qwen3:30b` | 0 | `Shinjuku-Shibuya Explorer` | This persona prioritizes convenient access to Shinjuku and Shibuya, values clean and well-equipped apartments, and appreciates responsive hosts. |
| `qwen2.5:1.5b` | 0 | validation失敗 | `Persona field 'recurring_expressions' ranks must be sorted ascending.` |

この比較から、30Bは大きいが今回のschema付き英語レビュー入力では日本語化の改善が見られず、1.5Bはschema追従が不安定だった。したがって、全クラスタ正式生成は `qwen3:4b` に固定した。

生成設計:

- 各クラスタから重心近傍の代表レビュー12件を抽出
- 各クラスタ3回生成
- JSON schema modeを使用
- `think=False`
- `temperature=0.0`
- 必須フィールドとlabel enumを検証
- `recurring_expressions` は単語頻度ではなく意味レベル表現をrank 1から5で出力
- 各priority / pain point / recurring expressionにreview idとevidence phraseを付与

生成評価:

| 指標 | 値 |
|---|---:|
| total clusters | 5 |
| generated clusters | 5 |
| coverage ratio | 1.0 |
| failure clusters | 0 |
| total failures | 0 |
| repetitions | 3 |
| mean name consistency | 1.0 |
| min name consistency | 1.0 |
| recurring expression count mean | 5.0 |
| priority count mean | 2.2 |
| confidence high | 5 |
| passed | true |

反復生成ごとのpersona name:

| cluster | selected persona_name | repetition 1 | repetition 2 | repetition 3 | stability |
|---:|---|---|---|---|---:|
| 0 | `Shinjuku/Shibuya Explorer` | `Shinjuku/Shibuya Explorer` | `Shinjuku/Shibuya Explorer` | `Shinjuku/Shibuya Explorer` | 3/3 |
| 1 | `Tokyo City Explorers` | `Tokyo City Explorers` | `Tokyo City Explorers` | `Tokyo City Explorers` | 3/3 |
| 2 | `Kitchen-focused travelers` | `Kitchen-focused travelers` | `Kitchen-focused travelers` | `Kitchen-focused travelers` | 3/3 |
| 3 | `Urban Commuter` | `Urban Commuter` | `Urban Commuter` | `Urban Commuter` | 3/3 |
| 4 | `Tokyo Urban Traveler` | `Tokyo Urban Traveler` | `Tokyo Urban Traveler` | `Tokyo Urban Traveler` | 3/3 |

出力:

- `reports/persona_definitions.json`
- `reports/persona_generation_metrics.json`

`persona_generation_failures.json` は失敗0の場合に残らないよう修正済み。

考察:

- JSON schema mode、`temperature=0.0`、3回反復生成により、構造化出力の安定性は高い。実測でもcoverage `1.0`、failure `0`、name consistency `1.0` だった。
- `recurring_expressions` を単語頻度ではなく意味レベル表現として出力させたことで、`station`, `clean`, `host` のような断片ではなく、「駅や主要エリアへアクセスしやすい」「ホストの返信が早い」「キッチン設備が揃っている」のように議論可能な粒度になった。
- 一方で、生成モデルは英語レビューとJSON schemaに引っ張られ、`output_language: Japanese` 指定でも英語出力になりやすかった。したがって、本レポートでは分析用にペルソナ名以外を日本語訳した付録を追加する。
- evidence phraseは監査可能性のため原文を残すのが理想である。日本語訳だけにすると、後から元レビューと照合しにくくなる。

## 10. 生成されたペルソナ

| cluster | persona_name | confidence | sentiment | price sensitivity | recurring expressions |
|---:|---|---|---|---|---:|
| 0 | `Shinjuku/Shibuya Explorer` | high | positive | low | 5 |
| 1 | `Tokyo City Explorers` | high | positive | unknown | 5 |
| 2 | `Kitchen-focused travelers` | high | positive | low | 5 |
| 3 | `Urban Commuter` | high | positive | unknown | 5 |
| 4 | `Tokyo Urban Traveler` | high | positive | low | 5 |

各ペルソナには、移動利便性、観光地への近さ、ホスト応答、清潔さ、キッチン設備、空間の狭さなどの根拠付き表現が含まれている。

考察:

- 5クラスタはいずれもpositive傾向であり、Airbnbレビューの全体的なpositive偏りを反映している。ペルソナ間の差は感情極性よりも、立地、観光導線、キッチン設備、通勤・交通、清潔さ、空間制約に出ている。
- `Kitchen-focused travelers` のように設備利用目的が明確なクラスタが出ている点は有益である。単なる地域別クラスタではなく、宿泊体験上の具体的なニーズが抽出されている。
- 一方で、`Shinjuku/Shibuya Explorer`, `Tokyo City Explorers`, `Tokyo Urban Traveler` など、交通・観光利便性を中心とするペルソナが複数ある。これはTokyo Airbnbレビューでは立地利便性が非常に強い共通軸であることを示すが、差別化には代表レビューや地理情報との追加照合が必要である。

## 11. 既知の制約

1. `qwen3:4b` は `output_language: Japanese` を指定しても、英語レビューとJSON schema生成中では英語出力に寄る。JSON構造、label enum、根拠追跡は安定しているため、今回の正式成果物は英語ペルソナJSONとして扱うのが妥当である。
2. 一部レビュー本文には元データ由来の文字化け片が残る。これはembedding前のcleaning段階で `ftfy` 等による文字修復を入れて全工程を再実行すると改善できる。
3. occupancy proxy validationは `pearson_r=0.0382`、`passed=false` だった。これはペルソナ生成までは直接阻害しないが、後続の稼働率分析ではproxyの扱いに注意が必要である。
4. clusteringのnoise ratioは高い。ペルソナは生成できているが、クラスタリング感度分析として `min_cluster_size_ratio` やUMAP/HDBSCAN設定の再探索が有益である。

## 12. 判定

ペルソナ生成までの完全実験は完了した。特に、Airbnb由来の3か月teacherでfine-tuneしたencoderが、別3か月の感情評価データで明確な改善を示し、そのfine-tuned encoderで全528,718レビューをembeddingしたうえで、5クラスタすべてに対して根拠付きペルソナを生成できた。

研究上の主な改善余地は、文字化け修復、クラスタnoise ratio低減、日本語ペルソナ出力に強いLLMまたは翻訳段の追加である。

## 13. ペルソナ生成OUTPUTの日本語版

以下は `reports/persona_definitions.json` の内容を、ペルソナ名以外は日本語で読めるように整理したものである。`sentiment_tendency.label`、`price_sensitivity.label`、`confidence` は機械可読labelとして英語値を併記する。根拠レビューIDは原JSONの監査用IDである。根拠phraseは、原文照合を重視する場合は `reports/persona_definitions.json` を参照する。

### Cluster 0: `Shinjuku/Shibuya Explorer`

目的: 東京の主要エリアを、利便性と快適さを保ちながら探索する。

頻出表現:

| rank | 表現 | 根拠の要約 | 主な根拠review_id |
|---:|---|---|---|
| 1 | 新宿・渋谷へ短い徒歩移動や鉄道でアクセスしやすい | 複数レビューで、新宿・渋谷の両方に近く、徒歩または短時間移動で行ける点が繰り返し述べられている。 | `1272940857806249522`, `997473226523752799`, `1439564784937904630`, `1289508302339432667`, `1409195590167049014`, `1377244409530727786`, `543049101`, `1489654598862709996`, `447109341`, `1111988683236624788`, `1317120321753201212`, `1419325515170561277` |
| 2 | ホストの返信が早く、先回りしたコミュニケーションがある | ホストの迅速さ、親切さ、チェックイン説明の明確さが繰り返し評価されている。 | `1272940857806249522`, `997473226523752799`, `1439564784937904630`, `1409195590167049014`, `1377244409530727786`, `1489654598862709996`, `447109341`, `1111988683236624788`, `1317120321753201212`, `1419325515170561277` |
| 3 | コンパクトだが基本設備は揃っている | 部屋は狭いが、短期滞在に必要な設備や清潔さは満たしているという評価が多い。 | `1439564784937904630`, `1409195590167049014`, `1377244409530727786`, `1489654598862709996`, `1111988683236624788`, `1317120321753201212` |
| 4 | 飲食店・スーパー・コンビニなど周辺施設へ歩いて行ける | レストラン、スーパー、7-Eleven、公共交通への近さが複数レビューで言及されている。 | `997473226523752799`, `1439564784937904630`, `1289508302339432667`, `1489654598862709996`, `447109341`, `1111988683236624788`, `1317120321753201212` |
| 5 | 荷物を持った移動ではエレベーターなしが負担になる | 狭さや階段、大きなスーツケースとの相性が制約として繰り返し現れる。 | `1439564784937904630`, `1409195590167049014`, `1377244409530727786`, `1489654598862709996`, `1111988683236624788`, `1317120321753201212` |

重視点:

- 主要エリアへの徒歩・鉄道アクセス: 新宿・渋谷への近さが最も強い価値として出ている。
- ホストコミュニケーション: 返信の速さ、明確な案内、親切な対応が満足度を支えている。

課題:

- コンパクトな空間と座る場所の少なさ: くつろぐ席や大きな荷物には制約がある。
- 荷物移動時のエレベーターなし: 階段とスーツケースの相性が弱点になる。

感情傾向: `positive`。小さな空間制約はあるが、立地と利便性への満足が強い。  
価格感度: `low`。価格よりも立地と設備の価値が強く語られている。  
ホスト向け施策:

- チェックイン手順と連絡導線を明確にし、返信速度を維持する。
- 新宿・渋谷への徒歩・交通アクセスを listing 上で明確に示す。
- 短期滞在向きのコンパクトな部屋であること、荷物スペースの制約を事前に伝える。

confidence: `high`  
説明: 東京の主要エリアを巡る旅行者で、新宿・渋谷への歩きやすさとホストの返信速度を重視する。空間の狭さやエレベーターなしは、短期滞在では許容されるが、事前説明が必要な注意点である。

### Cluster 1: `Tokyo City Explorers`

目的: 東京の都市観光スポットを便利に巡る。

頻出表現:

| rank | 表現 | 根拠の要約 | 主な根拠review_id |
|---:|---|---|---|
| 1 | 浅草寺、上野、秋葉原など主要観光地へアクセスしやすい | 浅草寺、雷門、上野、秋葉原、スカイツリー周辺への近さが繰り返し語られている。 | `1244661023394897367`, `1177204636630893691`, `811967201929261800`, `1134459398428056743`, `1438168799156158723`, `889467250039280199`, `1461328300519569709`, `856855357456476881`, `1464941685817047776`, `1401861290952998493`, `1388837836185502588`, `1460556473010128789` |
| 2 | ホストの返信が早く柔軟である | 迅速な返信、柔軟なチェックアウト対応、要望への反応が評価されている。 | `1177204636630893691`, `1134459398428056743`, `1464941685817047776` |
| 3 | 清潔で快適 | 清潔な部屋、快適な寝具、居心地の良さが複数レビューで出ている。 | `811967201929261800`, `1134459398428056743`, `1461328300519569709` |
| 4 | 家族やグループ向け設備がある | 複数シャワー・トイレ、家族滞在への適合が言及されている。 | `1177204636630893691`, `811967201929261800` |
| 5 | 公共交通へ歩いてアクセスできる | 駅や地下鉄への徒歩距離が観光導線として評価されている。 | `1244661023394897367`, `1177204636630893691`, `811967201929261800`, `1464941685817047776` |

重視点:

- 立地利便性: 観光名所と交通拠点の両方に近いことが最大の価値である。
- ホストの応答性: 早く柔軟なコミュニケーションが安心感を作っている。

課題:

- 温度への敏感さ: 一部レビューで室温が高いという不快感が示されている。

感情傾向: `positive`。立地、清潔さ、ホスト対応への満足が全体を占める。  
価格感度: `unknown`。価格に関する明示的な根拠は不足している。  
ホスト向け施策:

- 主要観光地への徒歩・交通アクセスを明確に示す。
- 連絡への即応と柔軟な対応を維持する。
- 複数バスルームなど、家族・グループ向け設備を明記する。

confidence: `high`  
説明: 東京観光の効率を重視する旅行者で、浅草・上野・秋葉原などへのアクセスとホストの応答性を評価する。清潔さと歩きやすさが強みで、温度管理は小さな改善点である。

### Cluster 2: `Kitchen-focused travelers`

目的: 滞在中に料理できるキッチン設備を必要とする短期滞在。

頻出表現:

| rank | 表現 | 根拠の要約 | 主な根拠review_id |
|---:|---|---|---|
| 1 | 料理に使えるキッチン設備が揃っている | キッチン用品、調理器具、設備の充実が繰り返し述べられている。 | `1485242318076579790`, `1172197427504200058`, `1098205595026240673`, `1317838921410639322`, `1454092600171447938`, `600406527612371730`, `1077214714218559331`, `1488930701656060070`, `610235812`, `1366333011905985827`, `933727792269129374` |
| 2 | 清潔でよく維持された宿泊空間 | 清潔さ、設備状態、管理状態が多くのレビューで評価されている。 | `1485242318076579790`, `1172197427504200058`, `1098205595026240673`, `1317838921410639322`, `1454092600171447938`, `600406527612371730`, `1077214714218559331`, `1488930701656060070`, `610235812`, `1366333011905985827`, `933727792269129374` |
| 3 | ホストのコミュニケーションが良く、返信も親切 | ホストやスタッフの親切さ、返信の良さが複数レビューで確認できる。 | `1454092600171447938`, `600406527612371730`, `1077214714218559331`, `1488930701656060070`, `610235812` |
| 4 | 観光スポットへアクセスしやすい立地 | 観光スポットへのアクセスの良さが一部レビューで言及されている。 | `600406527612371730` |
| 5 | 調理用品は概ね十分だが、もっと欲しいという声もある | キッチン設備は評価されている一方で、追加の調理用品が欲しいという不満もある。 | `1317838921410639322`, `1366333011905985827`, `933727792269129374` |

重視点:

- キッチン設備: 料理できるだけの器具や備品があることが中心的なニーズである。
- 清潔さ: キッチンを使うため、部屋全体と設備の清潔さが強く重視される。

課題:

- 調理用品の不足: 一部レビューでは、料理するには備品がもう少し必要だと示されている。

感情傾向: `positive`。キッチン設備、清潔さ、滞在体験への満足が強い。  
価格感度: `low`。価格や費用への不満は出ていない。  
ホスト向け施策:

- 調理用品をグループ人数と滞在目的に対して十分に用意する。
- 清潔さの水準を維持する。
- 返信の速さと親切な案内を維持する。

confidence: `high`  
説明: 滞在中に料理することを重視する旅行者で、清潔で設備の整ったキッチンを求める。全体的な満足度は高いが、調理用品の不足は改善余地として明確である。

### Cluster 3: `Urban Commuter`

目的: 交通拠点近くでの日常移動や短期滞在。

頻出表現:

| rank | 表現 | 根拠の要約 | 主な根拠review_id |
|---:|---|---|---|
| 1 | 駅とコンビニにアクセスしやすい | 駅、複数路線、コンビニ、スーパー、飲食店への近さが繰り返し示されている。 | `123559746`, `604902560`, `1438878132170654234`, `1422911301281603601`, `569563166`, `1468563176916911887`, `1269231858531127577`, `673534023127524358`, `855400701963976544`, `351451229`, `1307618439245516617`, `1178686687530968255` |
| 2 | ホストの返信が早く親切 | ホストが親切、返信が早い、質問に対応してくれるという記述が多い。 | `1438878132170654234`, `1422911301281603601`, `569563166`, `1269231858531127577`, `1178686687530968255` |
| 3 | 清潔で現代的な設備がある | 清潔さ、家のような快適さ、設備の良さが評価されている。 | `604902560`, `1269231858531127577`, `1178686687530968255` |
| 4 | 徒歩圏内に必要な施設がある | 駅、店舗、スーパー、コンビニが徒歩圏内にあることが価値として出ている。 | `1438878132170654234`, `1422911301281603601`, `1178686687530968255` |
| 5 | 短期滞在として価値が高い | 設備、立地、満足度から、短期滞在に対する価値が示されている。 | `604902560`, `1269231858531127577`, `1178686687530968255` |

重視点:

- 立地利便性: 駅、コンビニ、スーパー、飲食店へすぐ行けることが中心的価値である。
- ホストの応答性: 返信の速さと親切さが安心感を補強する。

課題:

- `unknown`: 具体的な不満点は代表レビュー内では明確に出ていない。

感情傾向: `positive`。`WOW`, `great`, `worth it`, `helpful` など強い肯定表現が多い。  
価格感度: `unknown`。価格への明示的な言及がなく判断できない。  
ホスト向け施策:

- ホストの返信速度を listing や運用上の強みとして維持する。
- 交通アクセスと周辺施設の利便性を強調する。
- 清潔さと現代的な設備を訴求する。

confidence: `high`  
説明: 交通と生活利便性を重視する短期滞在者で、駅・店舗・飲食店への近さと信頼できるホスト対応を求める。価格よりも、移動しやすさと滞在の安定性が重視されている。

### Cluster 4: `Tokyo Urban Traveler`

目的: 東京での短期都市探索。交通アクセスと周辺施設を重視する。

頻出表現:

| rank | 表現 | 根拠の要約 | 主な根拠review_id |
|---:|---|---|---|
| 1 | 駅へアクセスしやすい | 新宿方面、葛西駅、平井駅、山手線・中央線など、交通アクセスが繰り返し評価されている。 | `1301159217870587571`, `925750869898621295`, `1005409988891971718`, `1018441308620170538`, `1122154667869059443`, `1025014537717458229`, `933651102983309631`, `1107607656588735312`, `1433836880500816420` |
| 2 | 日本基準では広めで快適 | 日本の宿泊施設としては広い、3人でも快適などの表現が繰り返される。 | `1301159217870587571`, `1025014537717458229`, `1018441308620170538`, `1122154667869059443`, `933651102983309631`, `1433836880500816420` |
| 3 | ホストの返信が早い | ホストの返信、親切さ、助けになる対応が複数レビューで評価されている。 | `1301159217870587571`, `1025014537717458229`, `933651102983309631`, `1107607656588735312`, `1433836880500816420` |
| 4 | 共用・生活空間には制約がある | ソファベッド展開時の狭さ、階段、エレベーターなし、大きな荷物の運搬が課題として出る。 | `1005409988891971718`, `1018441308620170538`, `1122154667869059443`, `1433836880500816420` |
| 5 | 清潔さが重要な強み | 清潔、新しい、よく消毒されているという評価が繰り返される。 | `1301159217870587571`, `933651102983309631`, `1025014537717458229`, `1107607656588735312`, `1433836880500816420` |

重視点:

- 交通アクセス: 東京内を動き回るための駅近が中心的な価値である。
- 清潔さ: 快適性と安心感に直結する重要な評価軸である。
- ホストの応答性: 都市部滞在でのトラブル対応や不安解消に効いている。

課題:

- 狭い階段アクセス: 大きな荷物や複数人では階段が負担になる。
- 共用・生活空間の制約: ソファベッド利用時などに空間が狭くなる。
- 周辺インフラ由来の騒音: 消防署近くのサイレン音が一部レビューで問題として出ている。

感情傾向: `positive`。小さな課題はあるが、交通アクセス、清潔さ、ホスト対応が強く評価されている。  
価格感度: `low`。価格不満より、立地・清潔さ・価値への満足が目立つ。  
ホスト向け施策:

- 迅速な対応ができるホスト運用を維持し、問題解決の速さを訴求する。
- 駅への近さと東京各地への移動しやすさを明確に示す。
- 清掃・消毒基準を具体的に記載する。
- 階段、エレベーターなし、騒音可能性などを事前に明記する。

confidence: `high`  
説明: 東京での都市移動を重視する旅行者で、駅近、清潔さ、ホストの返信速度を重視する。空間や階段の制約はあるが、立地と滞在品質がそれを上回る価値として評価されている。
