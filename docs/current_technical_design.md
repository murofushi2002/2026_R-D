# SentiPersona-Airbnb 現行技術設計書

作成日: 2026-06-04  
対象実装: `src/sentipersona_airbnb` / `configs/experiment.example.yaml`

## 1. 目的

Inside Airbnb のレビューから宿泊者ペルソナを発見し、そのペルソナ比率と月次の occupancy proxy の関係を評価する。

現在の設計方針は次の通り。

- 外部口コミデータセットは使わない。Kaggle、TripAdvisor、Booking.com 系の教師データは使わず、Inside Airbnb の中で完結する。
- 追加学習用の感情疑似ラベル生成と SentiCSE fine-tune は最新3か月レビューで行う。
- fine-tuned encoder の評価は、学習に使わない別の3か月レビューで行う。
- 本番の embedding、clustering、persona 生成、timeseries、evaluation は全レビューで行う。
- レビュー本文の単語数による除外や切り詰めは行わない。空文字、URL/PII処理後に空になるもの、日付欠損、言語フィルタ不一致のみを除外する。

## 2. 全体アーキテクチャ

```text
Inside Airbnb
  reviews.csv.gz / listings.csv.gz / calendar.csv.gz
        |
        v
preprocess-airbnb
  - text cleaning
  - date normalization
  - language filtering
  - listing metadata merge
  - production all-review file
  - fine-tune 3-month window
  - sentiment-eval 3-month window
  - occupancy proxies
        |
        +--> airbnb_reviews_clean_all.parquet
        |        |
        |        v
        |     embed -> cluster -> personas -> timeseries -> evaluate
        |
        +--> airbnb_reviews_finetune_window.parquet
        |        |
        |        v
        |     label-airbnb-sentiment -> teacher_reviews.parquet -> train
        |
        +--> airbnb_reviews_sentiment_eval_window.parquet
                 |
                 v
              label-airbnb-sentiment -> sentiment_eval_reviews.parquet
                 |
                 v
              evaluate-sentiment-encoder
```

## 3. 主要成果物

| 用途 | ファイル |
|---|---|
| 本番用全レビュー | `data/processed/airbnb_reviews_clean_all.parquet` |
| 旧名互換 | `data/processed/airbnb_reviews_clean.parquet` |
| fine-tune用3か月レビュー | `data/processed/airbnb_reviews_finetune_window.parquet` |
| 評価用3か月レビュー | `data/processed/airbnb_reviews_sentiment_eval_window.parquet` |
| fine-tune窓の感情疑似ラベル | `data/processed/airbnb_reviews_finetune_sentiment.parquet` |
| 評価窓の感情疑似ラベル | `data/processed/airbnb_reviews_sentiment_eval.parquet` |
| fine-tune teacher | `data/interim/teacher_reviews.parquet` |
| sentiment encoder 評価データ | `data/interim/sentiment_eval_reviews.parquet` |
| 全レビューembedding | `data/processed/airbnb_review_embeddings.npy` |
| クラスタID | `data/processed/regional_cluster_labels.npy` |
| ペルソナ定義 | `reports/persona_definitions.json` |
| ペルソナ生成評価 | `reports/persona_generation_metrics.json` |
| sentiment encoder 評価 | `reports/sentiment_embedding_eval.json` |

## 4. 技術選定理由

### 4.1 Inside Airbnb

Inside Airbnb はレビュー、listing、calendar を都市単位で取得でき、研究用途で扱いやすい。外部ホテルレビューを使わないことで、ホテル文脈からAirbnb文脈へのドメインシフトを避けられる。

選定理由:

- Airbnbドメイン内で teacher 作成、fine-tune、評価まで閉じられる。
- review date、listing id、calendar があり、テキスト分析と時系列proxy分析を接続できる。
- 公開データで再現性を担保しやすい。

注意:

- calendar は実稼働率ではない。`available == f` は予約済み日とホストブロック日を区別できないため、occupancy proxy として扱う。

### 4.2 fastText language identification

標準 sentiment model が英語モデルであるため、英語レビューに揃える必要がある。fastText LID は軽量で、多言語レビューが混在するInside Airbnbに対して実用的である。

選定理由:

- 176言語対応で混在言語に強い。
- 推論が軽く、全レビュー前処理に使いやすい。
- `strict_language_filter: false` により、モデル未取得時の実験継続も可能。

### 4.3 DistilBERT SST-2 sentiment model

`models/finetune` に配置した `distilbert/distilbert-base-uncased-finetuned-sst-2-english` を Airbnb 疑似ラベル器に使う。

選定理由:

- binary positive/negative の出力が明確で、`positive=1`, `negative=0` のteacherにしやすい。
- RoBERTa等より軽く、3か月分レビューの疑似ラベル生成に現実的。
- Hugging Face標準APIで再現しやすい。

注意:

- ラベルは真の正解ではなく疑似ラベルである。そのため confidence threshold、重複除去、class balancing、別3か月評価でノイズを管理する。

### 4.4 RoBERTa + supervised contrastive fine-tune

fine-tune対象は `models/sentense` に配置した `BAAI/bge-base-en-v1.5` の encoder で、mean pooling により文embeddingを作る。損失は supervised contrastive loss。

BGEを選定した理由:

- sentence embedding / feature extraction を主用途として公開されており、レビュー類似度、クラスタリング、代表レビュー抽出に向いている。
- RoBERTaのような汎用MLMより、downstream の embedding 品質を初期状態から期待できる。
- `bge-large` より軽く、全レビューembeddingまで含む本実験で品質と計算量のバランスがよい。
- sentiment contrastive fine-tune 後も、元のsemantic embedding能力を大きく壊しにくい実用的なサイズである。

選定理由:

- 感情極性をembedding空間に反映させやすい。
- 2クラス分類器そのものを作るのではなく、後段のクラスタリングに使える汎用embeddingを得られる。
- contrastive objective は「同極性を近く、異極性を遠く」という本研究の目的と合う。

### 4.5 UMAP + HDBSCAN

全レビューembeddingに対し、UMAPで非線形次元削減し、HDBSCANでクラスタリングする。

選定理由:

- UMAPは高次元sentence embeddingの局所構造を保ちやすい。
- HDBSCANはクラスタ数を事前に決めなくてよく、noise clusterを扱える。
- ペルソナ発見では、無理に全レビューをクラスタへ割り当てるより、曖昧なレビューをnoiseとして残す方が自然。

### 4.6 Ollama + Qwen3:4B

クラスタ代表レビューからpersona JSONを生成するため、ローカルLLMを使う。

選定理由:

- レビュー本文を外部APIに送らない。
- JSON schemaを指定し、下流の評価や可視化に使いやすい。
- `persona.repetitions` による反復生成で名前の安定性を評価できる。

### 4.7 統計評価 + XGBoost

ペルソナ比率とoccupancy proxyの関係は、相関、OLS、Granger、XGBoostで見る。

選定理由:

- 相関: 最小限の関係探索。
- OLS: 月ダミーやreview countを含めた説明可能な統計モデル。
- Granger: 月次ペルソナ比率がoccupancy proxyに先行するかの探索。
- XGBoost: 非線形な予測性能の確認。

## 5. 設定

標準設定は `configs/experiment.example.yaml`。

| キー | 標準値 | 役割 |
|---|---:|---|
| `data.target_city` | `Tokyo` | 対象都市 |
| `data.city_slug` | `tokyo` | Inside Airbnb URL探索 |
| `data.target_language` | `en` | 英語レビュー抽出 |
| `data.language_threshold` | `0.80` | fastText confidence閾値 |
| `data.finetune_review_window_months` | `3` | fine-tune teacher用月数 |
| `data.finetune_review_window_end` | `latest` | fine-tune窓の終端 |
| `data.sentiment_eval_review_window_months` | `3` | encoder評価用月数 |
| `data.sentiment_eval_review_window_end` | `before_finetune` | fine-tune窓直前を評価窓にする |
| `sentiment_labeling.min_confidence` | `0.95` | teacher採用閾値 |
| `sentiment_labeling.balance_classes` | `true` | train teacherのclass balancing |
| `sentiment_labeling.balance_eval_classes` | `true` | eval dataのclass balancing |
| `sentiment_labeling.model_name` | `models/finetune` | DistilBERT SST-2 疑似ラベル器 |
| `training.base_model` | `models/sentense` | BGE base encoder |
| `training.temperature` | `0.07` | contrastive loss温度 |
| `model_evaluation.max_samples_per_class` | `1000` | encoder評価のクラス別最大件数 |
| `clustering.n_components_cluster` | `50` | clustering用UMAP次元 |
| `clustering.min_cluster_size_ratio` | `0.02` | HDBSCAN最小クラスタ比 |
| `persona.ollama_model` | `qwen3:4b` | persona生成LLM |
| `occupancy.source` | `auto` | proxy自動選択 |

## 6. 前処理

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe preprocess-airbnb -c configs/experiment.example.yaml
```

### 6.1 テキストクリーニング

`clean_review` は以下だけを行う。

- HTML entity の復元
- URL削除
- メールアドレスを `[EMAIL]` にマスク
- 電話番号らしき文字列を `[PHONE]` にマスク
- 空白正規化
- 空文字の除外

単語数による `min_words` 除外や `max_words` 切り詰めは行わない。レビューが短くても、極端に長くても、本文情報を保持する。モデル入力時のtoken truncationは tokenizer 側の `max_length` で行う。

### 6.2 本番用全レビュー

言語フィルタ後の全レビューを本番母集団とする。

現在のTokyo snapshot `2025-09-29` の実測:

- クリーニング後レビュー: 1,004,917
- 英語フィルタ後の本番レビュー: 528,718
- 本番対象listing: 22,272

出力:

- `data/processed/airbnb_reviews_clean_all.parquet`

### 6.3 fine-tune用3か月窓

本番用全レビューから、最新3か月を teacher 作成用に切り出す。

現在の実測:

- 期間: `2025-07` から `2025-09`
- 件数: 41,601
- listing数: 14,344

出力:

- `data/processed/airbnb_reviews_finetune_window.parquet`

### 6.4 sentiment encoder評価用3か月窓

fine-tune用窓とは重ならない評価窓を作る。標準では `before_finetune` を指定しているため、fine-tune窓の直前3か月になる。

例:

- fine-tune: `2025-07` から `2025-09`
- sentiment encoder評価: `2025-04` から `2025-06`
- 評価窓レビュー: 61,453
- 評価窓listing: 15,048

出力:

- `data/processed/airbnb_reviews_sentiment_eval_window.parquet`

### 6.5 occupancy proxy

calendar-based:

```text
occupancy_rate = mean(available == "f") by listing_id, year_month
```

review-based:

```text
review_based_occupancy =
  clip((review_count / review_rate * length_of_stay) / days_in_month, 0, cap)
```

標準では calendar proxy と review-based proxy のPearson相関を検証し、相関が低ければreview-basedへfallbackする。

現在のTokyo実測:

- 検証ペア数: 8,539
- Pearson r: 0.0382
- p-value: 0.000410
- 判定: failed

## 7. 感情疑似ラベル生成

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe label-airbnb-sentiment -c configs/experiment.example.yaml
```

このコマンドは2つの窓をラベル付けする。

| 窓 | 入力 | 出力 |
|---|---|---|
| train | `airbnb_reviews_finetune_window.parquet` | `airbnb_reviews_finetune_sentiment.parquet`, `teacher_reviews.parquet` |
| eval | `airbnb_reviews_sentiment_eval_window.parquet` | `airbnb_reviews_sentiment_eval.parquet`, `sentiment_eval_reviews.parquet` |

処理:

1. OSS binary sentiment modelで `comments_clean` を分類。
2. `positive=1`, `negative=0` に正規化。
3. `min_confidence` 未満を除外。
4. `text` 重複を除外。
5. train/evalそれぞれでclass balancingを行う。

eval側は fine-tune に使わない。fine-tuned encoder の外部評価専用である。

## 8. SentiCSE Fine-tune

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe train -c configs/experiment.example.yaml
```

入力:

- `data/interim/teacher_reviews.parquet`

実装:

- `AutoModel` + mean pooling
- supervised contrastive loss
- `WeightedRandomSampler`
- AdamW
- linear warmup scheduler
- CUDA時のみ mixed precision

学習中評価:

- teacher内部の10% splitで SgTS を計算する。

出力:

- `models/senticse/<experiment-name>/`
- `reports/senticse_training_metrics.json`

## 9. Sentiment Encoder評価

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe evaluate-sentiment-encoder -c configs/experiment.example.yaml
```

入力:

- `data/interim/sentiment_eval_reviews.parquet`

評価対象:

- base encoder: `training.base_model`
- fine-tuned encoder: `models/senticse/<experiment-name>/`

評価指標:

| 指標 | 意味 |
|---|---|
| `same_sentiment_similarity` | 同じ感情ラベル同士の平均cosine類似度 |
| `different_sentiment_similarity` | 異なる感情ラベル同士の平均cosine類似度 |
| `sgts_delta` | same - different。大きいほど感情分離が良い |
| `silhouette_cosine` | 感情ラベルをクラスタと見なしたcosine silhouette |
| `centroid_cosine_distance` | positive重心とnegative重心のcosine距離 |

比較:

- `base`
- `fine_tuned`
- `improvement`

出力:

- `reports/sentiment_embedding_eval.json`

この評価は、teacher内部splitだけでは測れない「別時期レビューへの感情embedding一般化」を確認するために追加した。

## 10. 全レビューEmbedding

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe embed -c configs/experiment.example.yaml
```

入力:

- `data/processed/airbnb_reviews_clean_all.parquet`

モデル選択:

1. fine-tuned model directory が存在すればそれを使う。
2. 存在しなければ `training.base_model` を使う。

出力:

- `data/processed/airbnb_review_embeddings.npy`
- `reports/embedding_manifest.json`

整合条件:

```text
len(airbnb_reviews_clean_all.parquet) == len(airbnb_review_embeddings.npy)
```

## 11. Clustering

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe cluster -c configs/experiment.example.yaml
```

処理:

1. 全レビューembeddingを読み込む。
2. UMAPでclustering用低次元空間を作る。
3. HDBSCANでクラスタリングする。
4. noise ratio、silhouette、Davies-Bouldinを計算する。
5. 各クラスタのcentroidに近い代表レビューを保存する。

出力:

- `data/processed/regional_cluster_labels.npy`
- `data/processed/regional_cluster_probabilities.npy`
- `reports/regional_clustering_metrics.json`
- `reports/regional_cluster_samples.json`

## 12. Persona生成と評価

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe personas -c configs/experiment.example.yaml
```

入力:

- `reports/regional_cluster_samples.json`

LLM:

- Ollama `qwen3:4b`

要求schema:

- `persona_name`
- `purpose`
- `priorities`
- `sentiment_tendency`
- `price_sensitivity`
- `description`

評価を強化した点:

- 生成できたクラスタ割合 `coverage_ratio`
- LLM失敗数 `total_failures`
- 反復生成時の名前一致率 `name_consistency_by_cluster`
- 最小名前一致率 `min_name_consistency`
- 平均名前一致率 `mean_name_consistency`
- `evaluation.persona_name_consistency_min` に基づく `passed`

出力:

- `reports/persona_definitions.json`
- `reports/persona_generation_metrics.json`
- `reports/persona_generation_failures.json`、失敗時のみ

これにより、ペルソナ生成までの評価は「クラスタ品質」「代表レビュー」「LLM schema妥当性」「反復安定性」まで確認できる。

## 13. 時系列化

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe timeseries -c configs/experiment.example.yaml
```

処理:

1. 全レビューのcluster labelを `listing_id`, `year_month` で集計する。
2. `persona_<k>_ratio` を作る。
3. HDBSCAN probability があれば重みとして使う。
4. noise cluster `-1` は比率分母から除く。
5. review count重み付きrolling smoothingを行う。
6. `timeseries.lag_months` だけ月を戻してoccupancy proxyと結合する。

出力:

- `data/processed/monthly_persona_ratios.parquet`
- `data/processed/analysis_dataset.parquet`
- `reports/timeseries_manifest.json`

## 14. Occupancy関係評価

CLI:

```powershell
.\.venv\Scripts\sentipersona.exe evaluate -c configs/experiment.example.yaml
```

評価:

- Pearson correlation、lag 0-3
- OLS、HC3 robust covariance
- Granger causality test、最大lag 3
- XGBoost + TimeSeriesSplit

出力:

- `reports/correlation_results.csv`
- `reports/evaluation_summary.json`

## 15. 標準実験手順

```powershell
.\scripts\bootstrap.ps1
ollama pull qwen3:4b
.\scripts\run_experiment.ps1 -Config configs/experiment.example.yaml
```

個別実行:

```powershell
.\.venv\Scripts\sentipersona.exe init -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe download -c configs/experiment.example.yaml --all
.\.venv\Scripts\sentipersona.exe preprocess-airbnb -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe validate-occupancy -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe label-airbnb-sentiment -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe train -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe evaluate-sentiment-encoder -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe embed -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe cluster -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe personas -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe timeseries -c configs/experiment.example.yaml
.\.venv\Scripts\sentipersona.exe evaluate -c configs/experiment.example.yaml
```

## 16. 評価設計の再チェック

ユーザー指摘前の不足:

- fine-tuned sentiment embedding model を、学習に使っていない別時期レビューで評価していなかった。
- persona生成はschema validation中心で、coverageや反復安定性の数値評価が不足していた。

今回追加した評価:

1. `sentiment_eval_review_window`: fine-tune窓とは別の3か月。
2. `sentiment_eval_reviews.parquet`: 評価専用疑似ラベルデータ。
3. `evaluate-sentiment-encoder`: base vs fine-tuned encoderの感情分離比較。
4. `persona_generation_metrics.json`: persona生成coverage、失敗数、名前一致率、passed判定。

現時点で、ペルソナ生成までに最低限必要な評価は以下で揃っている。

- teacher quality: ラベル分布、confidence平均、class balance
- encoder quality: SgTS、silhouette、centroid distance、base比較
- cluster quality: cluster count、noise ratio、silhouette、Davies-Bouldin
- persona quality: schema、coverage、反復名前一致率、失敗数

## 17. 既知の制約

- sentiment label は疑似ラベルであり真の人手ラベルではない。
- eval窓も同じOSS sentiment modelで疑似ラベル化するため、評価は「疑似ラベルに対する感情分離」である。
- occupancyは実測稼働率ではなくproxyである。
- LLM personaは生成揺らぎを持つため、最終報告では代表レビューとの対応を人手確認することが望ましい。
- 現環境ではCUDA対応PyTorchにより `NVIDIA GeForce RTX 3070 Laptop GPU` を認識し、fine-tuneと全レビューembeddingをGPUで実行済みである。
- `qwen3:4b` はJSON schema生成中に英語レビューへ引っ張られ、`output_language: Japanese` を指定しても英語ペルソナになりやすい。日本語成果物が必須なら、別LLMまたは翻訳段の追加評価が必要である。

## 18. 推奨Ablation

- fine-tuneなし base encoder
- fine-tune窓 1か月 / 3か月 / 6か月
- sentiment eval窓 直前3か月 / 別season 3か月
- confidence threshold `0.90` / `0.95` / `0.98`
- `occupancy.source: calendar` / `review_based`
- `timeseries.lag_months: 0` / `1` / `2`
- UMAP `n_components_cluster: 20` / `50` / `100`
- HDBSCAN `min_cluster_size_ratio: 0.01` / `0.02` / `0.05`
