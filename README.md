# SentiPersona-Airbnb

Inside Airbnb の全レビューを本番実験の母集団にし、感情軸で fine-tune した embedding から宿泊者ペルソナを生成して、月次の稼働率 proxy との関係を評価する実験環境です。

追加学習は計算負荷を抑えるため、Airbnb 口コミの最新3か月だけで行います。さらに、その直前3か月を評価用に疑似ラベル付けし、fine-tuned encoder が別時期レビューでも感情分離できるかを評価します。fine-tune 後の encoder は全レビューに対して embedding / clustering / persona / evaluation を実行します。

## Quick Start

```powershell
.\scripts\bootstrap.ps1
ollama pull qwen3:4b
.\scripts\run_experiment.ps1 -Config configs/experiment.example.yaml
```

ダウンロード済みデータで再実行する場合:

```powershell
.\scripts\run_experiment.ps1 -Config configs/experiment.example.yaml -SkipDownloads
```

## Pipeline

1. Inside Airbnb と fastText LID モデルを取得
2. Airbnb 全レビューをクリーニングし、`airbnb_reviews_clean_all.parquet` に保存
3. 全レビューから latest 3 months の `airbnb_reviews_finetune_window.parquet` を切り出し
4. fine-tune窓の直前3か月を `airbnb_reviews_sentiment_eval_window.parquet` として切り出し
5. 2つの3か月窓に OSS 感情分類モデルで positive/negative 疑似ラベルを付与
6. fine-tune窓の高信頼サンプルで SentiCSE fine-tune
7. 評価窓で base encoder と fine-tuned encoder の感情分離を比較
8. fine-tuned encoder で全レビューの embedding を生成
9. UMAP + HDBSCAN で地域ペルソナクラスタを抽出
10. Ollama `qwen3:4b` でペルソナ JSON を生成し、生成安定性を評価
11. 全レビュー由来の月次ペルソナ比率と稼働率 proxy を結合
12. クラスタ品質、SgTS、相関、予測性能を評価

## Main Commands

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

詳細は [docs/experiment_runbook.md](docs/experiment_runbook.md)、データ方針は [docs/data_sources.md](docs/data_sources.md)、環境レビューは [docs/experiment_environment_review.md](docs/experiment_environment_review.md) を参照してください。
