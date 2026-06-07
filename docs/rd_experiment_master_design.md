# SentiPersona Airbnb R&D 実験マスター設計書

作成日: 2026-06-06  
対象実験: Tokyo Airbnb review based sentiment-persona discovery and occupancy analysis  
実装パッケージ: `sentipersona_airbnb`  
標準config: `configs/experiment.example.yaml`

## 1. 研究目的

本研究開発では、Airbnbの口コミレビューから宿泊者の潜在的な嗜好・不満・期待を抽出し、地域または物件群ごとのペルソナとして構造化する。さらに、生成されたペルソナ比率の時系列変化が、稼働率proxyとどの程度関係するかを評価する。

中心的な問いは以下である。

1. Airbnbレビュー全体から、宿泊者の意味的・感情的なまとまりを安定したクラスタとして抽出できるか。
2. 感情ラベルで追加学習したembedding encoderは、未使用期間のレビューでもpositive/negativeの分離を改善するか。
3. クラスタ代表レビューから生成したペルソナは、反復生成しても一貫した属性を持つか。
4. 月次のペルソナ比率は、稼働率proxyの説明・予測に有用か。

本実験の重要な設計方針は、追加学習の計算負荷を抑えつつ、本番の下流分析では全レビューを使うことである。

## 2. 実験全体の設計思想

本実験では、口コミ感情の追加学習に使うデータと、本番のペルソナ発見に使うデータを明確に分離する。

| 用途 | データ | 範囲 |
|---|---|---|
| 本番embedding / clustering / persona / 評価 | `airbnb_reviews_clean_all.parquet` | 前処理・言語filter後の全レビュー |
| 追加学習用teacher作成 | `airbnb_reviews_finetune_window.parquet` | 最新3か月 |
| sentiment encoder評価 | `airbnb_reviews_sentiment_eval_window.parquet` | fine-tune窓の直前3か月 |
| teacher high confidence labels | `teacher_reviews.parquet` | 最新3か月の高信頼positive/negative |
| encoder評価用labels | `sentiment_eval_reviews.parquet` | 評価3か月の高信頼positive/negative |

この分離により、以下を避ける。

- 追加学習用データと評価データの時系列リーク
- 計算負荷の大きい疑似ラベル付けを全レビューに実施すること
- fine-tune済みencoderの効果を、学習に使った同じレビューだけで評価すること

一方で、本番のペルソナ生成では全レビューをembeddingするため、発見されるペルソナは最新3か月に限定されない。

## 3. 現在の実装済みパイプライン

CLIは `sentipersona` で提供される。

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

ダウンロード済みデータとローカルモデルを使う場合は以下を使う。

```powershell
.\scripts\run_experiment.ps1 -Config configs/experiment.example.yaml -SkipDownloads
```

## 4. データ設計

### 4.1 データソース

主データはInside AirbnbのTokyo snapshotである。Kaggleの既存sentiment datasetは使用しない。Airbnbレビュー自体にOSS sentiment modelで疑似ラベルを付け、そのラベルでAirbnbドメイン向けにencoderを追加学習する。

使用ファイル:

- `reviews.csv.gz`
- `listings.csv.gz`
- `calendar.csv.gz`

現在確認済みsnapshot:

- `data/raw/inside_airbnb/tokyo/2025-09-29`

### 4.2 前処理

`clean_review` では以下のみを行う。

- HTML entity復元
- URL削除
- emailを `[EMAIL]` に置換
- phone numberを `[PHONE]` に置換
- 連続空白の正規化
- 空文字の除外

重要: `min_words` 未満の除外や `max_words` 超過分の切り詰めは行わない。短文レビューも長文レビューも原文情報を保持する。モデル入力時のtokenizer側では `max_length` によるtruncationが発生するが、保存済みデータ自体は切り詰めない。

### 4.3 言語filter

英語レビューを主対象にするため、fastText LIDを使う。

標準設定:

- `data.target_language: en`
- `data.language_threshold: 0.80`
- `data.strict_language_filter: false`

`strict_language_filter: false` のため、fastTextモデルが存在しない場合でも実験は止めない。ただし現在は `models/language/lid.176.bin` が配置済みである。

### 4.4 実測済みデータ件数

`reports/airbnb_data_quality.json` に基づく現在の実測値:

| 項目 | 値 |
|---|---:|
| cleaning後レビュー数 | 1,004,917 |
| 言語filter後の本番レビュー数 | 528,718 |
| 本番対象listing数 | 22,272 |
| fine-tune窓 | 2025-07 から 2025-09 |
| fine-tune窓レビュー数 | 41,601 |
| fine-tune窓listing数 | 14,344 |
| sentiment encoder評価窓 | 2025-04 から 2025-06 |
| 評価窓レビュー数 | 61,453 |
| 評価窓listing数 | 15,048 |
| calendar月次行数 | 363,285 |
| review-based occupancy行数 | 269,451 |

## 5. モデル選定

### 5.1 感情ラベル生成モデル

採用モデル:

- Hugging Face: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- ローカル配置: `models/finetune`
- 用途: Airbnbレビューへのpositive/negative疑似ラベル付け

必要ファイル:

- `config.json`
- `model.safetensors`
- `tokenizer_config.json`
- `vocab.txt`

選定理由:

1. SST-2の二値sentiment classificationに特化している。
2. DistilBERTのため軽量で、大量レビューへの疑似ラベル付けに使いやすい。
3. 出力がpositive/negativeに整理しやすく、`positive=1`, `negative=0` のteacher datasetを作れる。
4. 本研究ではラベル生成器そのものを最終成果にしないため、重いLLMによる全件ラベル付けより、信頼度閾値で高精度サンプルだけ採用する方が実験設計として安定する。

設計上の注意:

- SST-2は一般英語sentimentであり、Airbnbドメイン固有の複合感情を完全には捉えない。
- そのため `sentiment_labeling.min_confidence: 0.95` を設定し、高信頼サンプルのみをteacherとして使う。
- 疑似ラベルのcoverageとclass balanceは `reports/airbnb_sentiment_labeling.json` で確認する。

### 5.2 embedding base model

採用モデル:

- Hugging Face: `BAAI/bge-base-en-v1.5`
- ローカル配置: `models/sentense`
- 用途: fine-tune前後のsentence embedding encoder

必要ファイル:

- `config.json`
- `model.safetensors`
- `tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `vocab.txt`
- `modules.json`
- `sentence_bert_config.json`
- `config_sentence_transformers.json`

選定理由:

1. BGEはsentence embedding / feature extractionを主用途とするモデルである。
2. 汎用MLMであるRoBERTaより、初期状態から類似度計算・クラスタリング・代表レビュー抽出に向く。
3. `bge-large` と比べて計算負荷が軽く、50万件規模の全レビューembeddingに現実的である。
4. 768次元embeddingのため、UMAPやHDBSCANとの接続が扱いやすい。
5. 感情contrastive fine-tune後もsemantic embedding能力を極端に壊しにくいサイズである。

補足:

- フォルダ名は `models/sentense` で運用している。スペルは `sentence` ではないが、configがこのパスを参照しているため実験上は問題ない。
- 実装では `AutoTokenizer(..., use_fast=False)` と `AutoModel.from_pretrained(...)` でロードする。

### 5.3 persona generation model

採用モデル:

- `qwen3:4b`
- 実行基盤: Ollama
- 用途: クラスタ代表レビューからペルソナJSONを生成

選定理由:

1. ローカルLLMであり、レビュー本文を外部APIへ送らない。
2. JSON schemaをpromptで固定でき、後段評価に接続しやすい。
3. 反復生成 `persona.repetitions: 3` により、persona name consistencyを評価できる。
4. 4B規模でCPU環境でも試行可能な範囲にある。

## 6. 疑似ラベル設計

### 6.1 train teacher

入力:

- `data/processed/airbnb_reviews_finetune_window.parquet`

出力:

- `data/processed/airbnb_reviews_finetune_sentiment.parquet`
- `data/interim/teacher_reviews.parquet`

処理:

1. `models/finetune` でレビュー本文をpositive/negative分類する。
2. `sentiment_score >= 0.95` のみ採用する。
3. `positive=1`, `negative=0` として `label_id` を保存する。
4. class imbalanceを抑えるため、標準ではpositive/negativeをbalanced samplingする。

### 6.2 sentiment encoder評価データ

入力:

- `data/processed/airbnb_reviews_sentiment_eval_window.parquet`

出力:

- `data/processed/airbnb_reviews_sentiment_eval.parquet`
- `data/interim/sentiment_eval_reviews.parquet`

目的:

- fine-tuneに使っていない別の3か月で、base encoderとfine-tuned encoderの感情分離性能を比較する。

## 7. Fine-tune設計

### 7.1 モデル構造

`SentimentEncoder` は以下で構成される。

- tokenizer: `AutoTokenizer.from_pretrained(training.base_model, use_fast=False)`
- encoder: `AutoModel.from_pretrained(training.base_model)`
- pooling: attention maskを使ったmean pooling

出力embeddingはレビュー文単位の768次元ベクトルである。

### 7.2 損失関数

追加学習ではsupervised contrastive lossを使う。

目的:

- 同じsentiment labelのレビューembeddingを近づける。
- 異なるsentiment labelのレビューembeddingを離す。

標準設定:

- `training.temperature: 0.07`
- `training.epochs: 5`
- `training.batch_size: 32`
- `training.learning_rate: 0.00002`
- `training.max_length: 256`
- `training.mixed_precision: true`

本実験はGPU実行を前提にする。実装は `torch.cuda.is_available()` が `true` の場合、自動的に `cuda` を選択する。GPUが使える場合、感情ラベル付け、fine-tune、全レビューembeddingで大きな速度改善が見込める。

現在のvenvで確認した結果:

```text
torch=2.8.0+cu128
cuda_available=True
cuda_device_count=1
cuda_version=12.8
device_name=NVIDIA GeForce RTX 3070 Laptop GPU
```

この結果により、今回の本実験ではCUDAを利用できる。再実行前の確認コマンドは以下である。

```powershell
.\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"
```

mixed precisionは `training.mixed_precision: true` で有効化済みであり、deviceが `cuda` の場合のみ `torch.cuda.amp` が有効になる。CPU環境では自動的に無効になる。

### 7.3 モデル保存

出力:

- `models/senticse/tokyo_senti_persona/`

保存内容:

- fine-tuned encoder
- tokenizer
- `reports/senticse_training_metrics.json`

## 8. Sentiment Encoder評価

評価コマンド:

```powershell
.\.venv\Scripts\sentipersona.exe evaluate-sentiment-encoder -c configs/experiment.example.yaml
```

入力:

- `data/interim/sentiment_eval_reviews.parquet`

比較対象:

- base encoder: `models/sentense`
- fine-tuned encoder: `models/senticse/tokyo_senti_persona/`

指標:

| 指標 | 意味 |
|---|---|
| SgTS same similarity | 同じsentiment同士の平均cosine similarity |
| SgTS different similarity | 異なるsentiment同士の平均cosine similarity |
| SgTS delta | same minus different |
| cosine silhouette | positive/negativeの分離度 |
| centroid distance | positive重心とnegative重心の距離 |

期待される結果:

- fine-tuned encoderの `sgts_delta` がbase encoderより大きい。
- fine-tuned encoderのsilhouetteが改善する。
- centroid distanceが増加する。

出力:

- `reports/sentiment_embedding_eval.json`

## 9. 全レビューEmbedding

入力:

- `data/processed/airbnb_reviews_clean_all.parquet`

使用モデル:

1. `models/senticse/tokyo_senti_persona/` が存在すればfine-tuned encoderを使う。
2. 存在しなければ `models/sentense` を使う。

出力:

- `data/processed/airbnb_review_embeddings.npy`
- `reports/embedding_manifest.json`

設計意図:

- 追加学習は最新3か月だけで行う。
- しかし本番のペルソナ発見は全レビュー528,718件に対して行う。
- これにより、fine-tuned encoderを全期間のレビュー表現へ適用する。
- GPU実行を前提に `embedding.batch_size: 256` を標準値とする。RTX 3070 Laptop GPUでは短いベンチでVRAM使用量約2.6GBを確認済みである。

## 10. Clustering設計

### 10.1 次元削減

UMAPを2種類使う。

| 用途 | 出力次元 | 設定 |
|---|---:|---|
| clustering用 | `n_components_cluster: 50` | `metric: cosine`, `min_dist: 0.0` |
| 可視化用 | `n_components_vis: 2` | `metric: cosine`, `min_dist: 0.1` |

UMAP選定理由:

- sentence embeddingの局所近傍構造を保ちやすい。
- HDBSCANの前処理として高次元ノイズを落とせる。
- 2次元可視化にも同じ枠組みを使える。
- 本番実験では50万件規模を完走させるため、`deterministic_umap: false`, `n_jobs: -1` とし、UMAPを並列実行する。
- 可視化用2次元は標準では別fitせず、clustering用UMAPの先頭2次元を保存する。これにより、全件UMAPを2回fitする計算負荷を避ける。

### 10.2 クラスタリング

HDBSCANを使う。

標準設定:

- `min_cluster_size_ratio: 0.02`
- `min_samples: 5`
- `cluster_selection_method: eom`

HDBSCAN選定理由:

- クラスタ数を事前に決めなくてよい。
- 密度の低いレビューをnoiseとして扱える。
- ペルソナ発見では無理に全レビューへクラスタを割り当てるより、曖昧なレビューをnoiseとして残す方が自然である。

評価指標:

- number of clusters
- noise ratio
- sampled silhouette (`metric_sample_size: 10000`)
- Davies-Bouldin score

出力:

- `data/processed/regional_cluster_labels.npy`
- `data/processed/regional_cluster_probabilities.npy`
- `data/processed/regional_umap_cluster.npy`
- `data/processed/regional_umap_vis.npy`
- `reports/regional_clustering_metrics.json`
- `reports/regional_cluster_samples.json`

## 11. Persona生成設計

入力:

- `reports/regional_cluster_samples.json`

各クラスタについて、UMAP空間の重心に近い代表レビューを `representative_reviews_per_cluster: 12` 件抽出する。

LLMには実装上、以下の完全なpromptを渡す。`{output_language}` には標準設定の `Japanese` が入り、`{numbered}` にはクラスタ代表レビューが番号付きで入る。

```text
You are generating data-grounded guest personas from Airbnb reviews.
Use only the evidence in the reviews. Do not invent demographics.
Do not infer age, gender, nationality, income, occupation, or family status
unless explicitly stated.
If evidence is insufficient, use "unknown" rather than guessing.
Avoid generic personas; make the persona specific to repeated evidence in this cluster.
Recurring expressions are not single keywords. They are short repeated meaning-level phrases
such as "easy access to train stations", "host responds quickly", or "room feels cramped".
Keep JSON keys and enum labels exactly in English.
Write generated free-text values in {output_language}: persona_name, purpose, expression,
why_recurring, free-form labels, basis, host_actions, and description.
Keep evidence_phrases in the original review language because they are evidence snippets.
Do not copy the English placeholder wording from the schema into the final values.

Reviews:
{numbered}

Return strict JSON only with this schema:
{
  "persona_name": "short memorable name",
  "purpose": "main travel/stay purpose inferred from reviews",
  "recurring_expressions": [
    {
      "rank": 1,
      "expression": "meaning-level expression, not a single keyword",
      "why_recurring": "why this expression appears repeatedly",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }
  ],
  "priorities": [
    {
      "label": "priority label",
      "basis": "why this is a priority",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }
  ],
  "pain_points": [
    {
      "label": "pain point label or unknown",
      "basis": "why this is a pain point, or unknown if evidence is insufficient",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }
  ],
  "sentiment_tendency": {
    "label": "positive|mixed|negative",
    "basis": "positive if praise dominates, negative if complaints dominate, mixed if both are salient",
    "evidence_review_ids": ["review_id"]
  },
  "price_sensitivity": {
    "label": "low|medium|high|unknown",
    "basis": "high when price/value/cheap/expensive is repeated, medium when value matters but not dominant, low when little price concern appears, unknown when evidence is insufficient",
    "evidence_review_ids": ["review_id"]
  },
  "host_actions": ["actionable recommendation grounded in repeated evidence"],
  "confidence": "low|medium|high",
  "description": "2-3 concise sentences"
}

Rules:
- Return 1 to 5 recurring_expressions, ordered by strength of repeated evidence.
- Every recurring_expression rank must be an integer from 1 to 5.
- Every priority and pain point must include evidence_review_ids and evidence_phrases.
- Use "unknown" for price_sensitivity or pain point labels when evidence is insufficient.
- Keep sentiment_tendency.label exactly one of: positive, mixed, negative.
- Keep price_sensitivity.label exactly one of: low, medium, high, unknown.
- Keep confidence exactly one of: low, medium, high.
- Do not include any text outside the JSON object.
```

Ollama呼び出しでは、上記promptに加えて実装側の `persona_json_schema()` を `format` に渡し、`think=False`、`temperature=0.0` で構造化JSON出力を固定する。これにより、JSON parse error、enum翻訳、必須フィールド欠落を抑える。

実装上の必須フィールド:

- `persona_name`
- `purpose`
- `recurring_expressions`
- `priorities`
- `pain_points`
- `sentiment_tendency`
- `price_sensitivity`
- `host_actions`
- `confidence`
- `description`

このpromptの意図:

- `Use only the evidence in the reviews` により、レビュー根拠のない属性推定を抑える。
- `Do not invent demographics` により、年齢、性別、国籍、職業などの危険な作り込みを避ける。
- `strict JSON only` により、後段の自動評価と時系列処理に接続しやすくする。
- `JSON keys and enum labels exactly in English` により、`positive`, `mixed`, `negative` などの機械可読labelを翻訳させない。
- `evidence_phrases` は原文維持とし、根拠片を後からレビュー本文へ照合しやすくする。
- `purpose`, `priorities`, `sentiment_tendency`, `price_sensitivity` を分けることで、宿泊目的、重視点、感情傾向、価格感度を議論可能な軸として保持する。

判定: 以前のschemaは「動く最小構成」ではあったが、研究用のベスト設計としては根拠追跡が弱かった。現在は evidence-grounded persona schema に更新し、単語頻度ではなく意味レベルの頻出表現をrank 1から5で出力する設計に変更した。

### 11.1 頻出表現の定義

`recurring_expressions` は単語頻度ではない。例えば `station`, `clean`, `host` のような単語単体ではなく、以下のような意味表現を抽出する。

- `easy access to train stations`
- `host responds quickly`
- `room feels cramped`
- `quiet despite central location`
- `good value for the location`

抽出基準:

1. 複数レビューで同じ意味が繰り返されている。
2. 単なる一般語ではなく、宿泊者の判断・期待・不満・行動に関係する。
3. 代表レビューの evidence phrase で説明できる。
4. rank 1 は最も強く反復する表現、rank 5 は相対的に弱いがまだクラスタ特徴として有用な表現とする。
5. 根拠が弱い場合は無理に5件出さず、1から5件の範囲で止める。

### 11.2 Label基準

`sentiment_tendency.label` の基準:

| label | 基準 |
|---|---|
| `positive` | praise, satisfaction, recommendation が中心で、明確な不満が少ない |
| `mixed` | praise と complaint がどちらも目立つ、または条件付き評価が多い |
| `negative` | complaint, disappointment, warning が中心で、満足表現が少ない |

`price_sensitivity.label` の基準:

| label | 基準 |
|---|---|
| `high` | price, cheap, expensive, value, worth など価格・費用対効果が繰り返し中心論点になる |
| `medium` | 価格・価値への言及はあるが、立地・清潔さ・設備などと同程度の副次論点である |
| `low` | 価格への不満や価値判断がほとんどなく、利便性・体験・設備が中心である |
| `unknown` | 価格感度を判断できる根拠が不足している |

`confidence` の基準:

| label | 基準 |
|---|---|
| `high` | 複数の代表レビューに同じ意味表現があり、evidence phrase が明確 |
| `medium` | 主要表現は見えるが、根拠レビュー数または表現の一貫性が限定的 |
| `low` | クラスタ内レビューが散らばっており、ペルソナ化に不確実性が残る |

`priorities.label` と `pain_points.label` は自由記述だが、必ず `basis`, `evidence_review_ids`, `evidence_phrases` を持つ。根拠が薄いpain pointは `unknown` とする。

反復生成:

- `persona.repetitions: 3`
- `persona.temperature: 0.0`

評価:

- 生成成功率
- coverage ratio
- persona name consistency
- priority count
- failure count

出力:

- `reports/persona_definitions.json`
- `reports/persona_generation_metrics.json`
- `reports/persona_generation_failures.json`

## 12. Occupancy proxy設計

### 12.1 calendar-based occupancy

`calendar.csv.gz` の `available == f` を予約済みまたは利用不可として扱い、月次平均を `occupancy_rate` とする。

出力:

- `data/processed/monthly_occupancy.parquet`

### 12.2 review-based occupancy

レビュー数から宿泊数を推定する。

式:

```text
estimated_booked_nights = review_count / review_rate * length_of_stay
review_based_occupancy = estimated_booked_nights / days_in_month
```

標準設定:

- `review_rate: 0.50`
- `default_length_of_stay: 3.0`
- `cap_review_based_occupancy: 0.70`

出力:

- `data/processed/review_based_occupancy.parquet`

### 12.3 proxy validation

calendar-basedとreview-basedのPearson correlationを測る。

現在の実測:

| 項目 | 値 |
|---|---:|
| n | 8,539 |
| pearson_r | 0.0382 |
| p_value | 0.000410 |
| passed | false |

解釈:

- calendar由来proxyとreview由来proxyの相関は非常に弱い。
- TokyoのInside Airbnb calendarは、予約済み・ブロック・ホスト都合の利用不可が混在する可能性がある。
- `occupancy.source: auto` では、検証に失敗した場合review-based proxyへfallbackする設計である。

## 13. 時系列分析設計

### 13.1 monthly persona ratio

全レビューのcluster labelから、listingごと月次のpersona比率を計算する。

出力:

- `data/processed/monthly_persona_ratios.parquet`

特徴量:

- `persona_<id>_ratio`
- `persona_<id>_smoothed`
- `review_count`
- `noise_ratio`

標準設定:

- `timeseries.smoothing_window: 3`
- `timeseries.min_monthly_reviews: 5`
- `timeseries.lag_months: 1`

### 13.2 analysis dataset

ペルソナ比率を1か月lagさせ、occupancy proxyと結合する。

出力:

- `data/processed/analysis_dataset.parquet`

目的:

- 当月のレビュー内容ではなく、前月以前のペルソナ構成が次月以降の稼働と関係するかを見る。

## 14. 最終評価設計

### 14.1 相関分析

各persona ratio / smoothed ratioとoccupancy_rateのPearson correlationを、lag 0から3で計算する。

出力:

- `reports/correlation_results.csv`

### 14.2 OLS

目的:

- persona featureがoccupancyをどの程度説明するかを線形モデルで確認する。

特徴量:

- persona smoothed ratio
- month dummy
- review_count

出力:

- `reports/evaluation_summary.json` 内の `ols`

### 14.3 Granger causality

目的:

- 地域集計されたpersona比率がoccupancyに先行する可能性を探索する。

注意:

- 因果を確定するものではない。
- 観測時系列が短い場合は不安定である。

### 14.4 XGBoost time series evaluation

目的:

- persona特徴量を含めた非線形モデルの予測性能を確認する。

評価:

- TimeSeriesSplit
- RMSE
- MAE
- R2

出力:

- `reports/evaluation_summary.json` 内の `xgboost`

## 15. 成果物一覧

### 15.1 data/processed

- `airbnb_reviews_clean_all.parquet`
- `airbnb_reviews_clean.parquet`
- `airbnb_reviews_finetune_window.parquet`
- `airbnb_reviews_sentiment_eval_window.parquet`
- `airbnb_reviews_finetune_sentiment.parquet`
- `airbnb_reviews_sentiment_eval.parquet`
- `airbnb_review_embeddings.npy`
- `regional_cluster_labels.npy`
- `regional_cluster_probabilities.npy`
- `regional_umap_cluster.npy`
- `regional_umap_vis.npy`
- `monthly_occupancy.parquet`
- `review_based_occupancy.parquet`
- `monthly_persona_ratios.parquet`
- `analysis_dataset.parquet`

### 15.2 data/interim

- `teacher_reviews.parquet`
- `sentiment_eval_reviews.parquet`

### 15.3 models

- `models/finetune`
- `models/sentense`
- `models/language/lid.176.bin`
- `models/senticse/tokyo_senti_persona/`

### 15.4 reports

- `airbnb_data_quality.json`
- `airbnb_sentiment_labeling.json`
- `senticse_training_metrics.json`
- `sentiment_embedding_eval.json`
- `embedding_manifest.json`
- `regional_clustering_metrics.json`
- `regional_cluster_samples.json`
- `persona_definitions.json`
- `persona_generation_metrics.json`
- `monthly_persona_timeseries_report.json`
- `occupancy_proxy_validation.json`
- `correlation_results.csv`
- `evaluation_summary.json`
- `run_all_outputs.json`

## 16. 現在の検証状況

実施済み:

- ローカルモデル配置確認
- DistilBERT SST-2の短文positive/negative推論確認
- BGE baseの768次元embedding出力確認
- `configs/experiment.example.yaml` のローカルモデル参照更新
- CUDA対応PyTorch導入とGPU認識確認
- `torch.cuda.is_available()`: `true`
- GPU: `NVIDIA GeForce RTX 3070 Laptop GPU`
- `pytest`: 16 passed
- `ruff`: passed
- `pip check`: passed
- `sentipersona init`: 成功
- Airbnb前処理完了
- occupancy proxy validation実行済み
- `label-airbnb-sentiment`: 成功
- `train`: 成功、`device=cuda`
- `evaluate-sentiment-encoder`: 成功
- `embed`: 成功、528,718件を768次元へencoding
- `cluster`: 成功、5クラスタ生成
- `personas`: 成功、5クラスタすべてで根拠付きpersona生成

今回の依頼範囲である「ペルソナ生成まで」は完了済みである。詳細な実行結果は `docs/persona_generation_experiment_report.md` にまとめた。

未実行または後続工程:

- `timeseries`
- `evaluate`

## 17. 技術的な論点

### 17.1 疑似ラベル品質

DistilBERT SST-2は汎用英語sentiment modelであり、Airbnb固有の文脈を完全には反映しない。例えば「small but cozy」はnegativeとpositiveが混ざる可能性がある。これに対して、本実験では高信頼predictionのみを採用し、さらに別期間でencoder評価を行う。

議論点:

- confidence `0.95` は厳しすぎるか。
- class balanceにより自然分布を歪めていないか。
- neutralやmixed sentimentを捨てることで、ペルソナ発見に必要なニュアンスが落ちないか。

### 17.2 BGEを感情fine-tuneする妥当性

BGEはsemantic embedding modelであり、sentiment専用ではない。supervised contrastive fine-tuneにより感情軸を強める一方で、宿泊目的や設備嗜好などのsemantic情報が弱まる可能性がある。

そのため、sentiment encoder評価だけでなく、クラスタ品質とpersona品質も同時に確認する必要がある。

議論点:

- SgTS改善とクラスタ品質改善は両立するか。
- sentiment軸が強くなりすぎて、全クラスタが単なるpositive/negative分割にならないか。
- base BGEとfine-tuned BGEのクラスタを比較するablationが必要か。

### 17.3 Clusteringの粒度

HDBSCANはクラスタ数を自動決定するが、UMAP次元数や `min_cluster_size_ratio` に敏感である。

議論点:

- `min_cluster_size_ratio: 0.02` は大規模レビューに対して粗すぎないか。
- 地域ペルソナを目的とするなら、大きいクラスタを優先すべきか、小さいニッチクラスタも拾うべきか。
- noise ratioが高い場合、それは失敗か、曖昧レビューを除外できている成功か。

### 17.4 Persona生成の妥当性

LLM personaは読みやすいが、代表レビューからの生成であるため、クラスタ全体を過度に単純化する危険がある。

対策:

- 代表レビューはクラスタ重心に近いものを使う。
- 反復生成でname consistencyを測る。
- evidenceをJSONに含め、レビュー根拠と結びつける。

議論点:

- persona name consistencyだけで十分か。
- evidence phraseが代表レビューに忠実かを自動評価する必要があるか。
- 人手評価を追加するべきか。

### 17.5 Occupancy proxyの限界

現在のcalendar-based proxyとreview-based proxyの相関は低い。これはoccupancy分析部分の解釈を慎重にする必要があることを示す。

議論点:

- calendar availabilityを稼働率とみなす妥当性
- review count由来proxyのreview_rate仮定
- occupancy評価を主要成果ではなく補助分析として扱うべきか

## 18. 推奨される追加実験

1. base BGE vs fine-tuned BGEのクラスタ比較
2. `min_confidence` を `0.90`, `0.95`, `0.98` で変えたteacher品質比較
3. fine-tune窓を3か月、6か月で比較
4. HDBSCANの `min_cluster_size_ratio` 感度分析
5. persona JSONに対する人手評価
6. occupancy proxyなしで、レビュー内評価スコアやlisting属性との関係分析
7. `bge-large-en-v1.5` への置換実験

## 19. 実験成功基準

最低限の成功条件:

- sentiment labelingでpositive/negativeの両classが十分数得られる。
- fine-tuned encoderのSgTS deltaがbase encoderより改善する。
- HDBSCANで複数クラスタが生成され、noise ratioが過大でない。
- persona生成coverageが高く、name consistencyが閾値以上である。
- downstream評価の成果物が全て生成される。

強い成功条件:

- fine-tuned encoderがsentiment分離を改善しつつ、クラスタ品質も維持または改善する。
- 生成ペルソナがレビュー根拠に基づき、クラスタ間で意味的に区別できる。
- persona ratioがoccupancy proxyまたはlisting評価指標に対して説明力を持つ。

## 20. まとめ

本実験環境は、Kaggleなどの外部sentiment datasetに依存せず、Airbnbレビュー自体から疑似ラベルを作り、Airbnbドメインに寄せたembedding encoderを追加学習する設計である。追加学習は最新3か月に限定し、評価は直前3か月、本番のペルソナ発見は全レビューで行う。

技術選定としては、疑似ラベル生成にDistilBERT SST-2、embedding baseにBGE base、クラスタリングにUMAP + HDBSCAN、ペルソナ生成にOllama + Qwen3:4Bを採用した。各技術は計算負荷、再現性、下流評価への接続性、ローカル実行可能性を重視して選ばれている。

今後の中心論点は、fine-tuned BGEが単にsentiment分離を改善するだけでなく、ペルソナ発見に必要なsemantic cluster品質を維持できるかである。そのため、SgTS、clustering metrics、persona generation metrics、時系列評価を一体で確認する必要がある。
