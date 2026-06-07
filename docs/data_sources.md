# Data Sources

## Inside Airbnb

- Main page: https://insideairbnb.com/get-the-data/
- Data assumptions: https://insideairbnb.com/data-assumptions/
- Default target in `configs/experiment.example.yaml`: Tokyo.
- Required files: `listings.csv.gz`, `reviews.csv.gz`, `calendar.csv.gz`.

The downloader discovers the latest matching city snapshot from the official Get the Data page.
After cleaning and language filtering, the production experiment keeps all available reviews in
`data/processed/airbnb_reviews_clean_all.parquet`.

Calendar `available == f` is tested as an occupancy proxy, with review-based occupancy used as a
validation signal because Inside Airbnb notes that booked nights and host-blocked nights are not
differentiated in the availability calendar. In `occupancy.source: auto`, the pipeline falls back to
review-based occupancy when the validation correlation is below the configured threshold.

## Supervised Sentiment Teacher Data

No external review dataset is used. The pipeline creates supervised fine-tuning data from Inside
Airbnb itself:

- Clean `reviews.csv.gz`.
- Keep all cleaned/language-filtered reviews for production downstream steps.
- Slice the configured fine-tune window from the production reviews. The default is the latest 3
  calendar months by review date:
  `data.finetune_review_window_months: 3`, `data.finetune_review_window_end: latest`.
- Store that slice in `data/processed/airbnb_reviews_finetune_window.parquet`.
- Slice a separate sentiment-encoder evaluation window. The default is the 3 calendar months before
  the fine-tune window:
  `data.sentiment_eval_review_window_months: 3`,
  `data.sentiment_eval_review_window_end: before_finetune`.
- Store that slice in `data/processed/airbnb_reviews_sentiment_eval_window.parquet`.
- Run an OSS binary sentiment model over both 3-month slices.
- Keep only high-confidence positive/negative predictions.
- Store `positive=1` and `negative=0` in `data/interim/teacher_reviews.parquet`.
- Store separate evaluation labels in `data/interim/sentiment_eval_reviews.parquet`.

Default sentiment labeler:

- Hugging Face model: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- Local path: `models/finetune`

Default embedding base:

- Hugging Face model: `BAAI/bge-base-en-v1.5`
- Local path: `models/sentense`
- Default confidence threshold: `0.95`
- Default class strategy: balanced sampling between positive and negative samples.

## Language Identification

- fastText LID model: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

The model is optional unless `data.strict_language_filter: true`. With Tokyo data and an English
sentiment-labeling model, the default keeps English reviews using `target_language: en`.
