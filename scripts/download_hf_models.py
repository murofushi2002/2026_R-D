import traceback

from transformers import (
    AutoModel,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DistilBertTokenizer,
)


def main() -> None:
    sentiment_model = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    encoder_model = "BAAI/bge-base-en-v1.5"

    print(f"Downloading tokenizer: {sentiment_model}", flush=True)
    DistilBertTokenizer.from_pretrained(sentiment_model)
    print(f"Downloading sequence classifier: {sentiment_model}", flush=True)
    AutoModelForSequenceClassification.from_pretrained(sentiment_model)
    print(f"Downloading tokenizer: {encoder_model}", flush=True)
    AutoTokenizer.from_pretrained(encoder_model, use_fast=False)
    print(f"Downloading encoder: {encoder_model}", flush=True)
    AutoModel.from_pretrained(encoder_model)
    print("downloaded")


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        traceback.print_exc()
        raise
