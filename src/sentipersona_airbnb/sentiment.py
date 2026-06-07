from __future__ import annotations

from typing import Any

import pandas as pd
import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, DistilBertTokenizer

from .config import cfg_get, standard_files, standard_paths
from .utils import write_json


def normalize_binary_sentiment(
    raw_label: str,
    positive_labels: list[str],
    negative_labels: list[str],
) -> str | None:
    label = raw_label.strip().lower()
    positives = {item.strip().lower() for item in positive_labels}
    negatives = {item.strip().lower() for item in negative_labels}
    if label in positives:
        return "positive"
    if label in negatives:
        return "negative"
    return None


@torch.no_grad()
def predict_binary_sentiment(
    texts: list[str],
    model_name: str,
    batch_size: int,
    max_length: int,
    positive_labels: list[str],
    negative_labels: list[str],
    device: str | None = None,
) -> pd.DataFrame:
    columns = [
        "text",
        "sentiment",
        "sentiment_id",
        "sentiment_score",
        "raw_sentiment_label",
        "source",
    ]
    if not texts:
        return pd.DataFrame(columns=columns)

    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    model.eval()
    id2label = {int(key): value for key, value in model.config.id2label.items()}

    rows: list[dict[str, Any]] = []
    for start in tqdm(range(0, len(texts), batch_size), desc="sentiment labeling"):
        batch_texts = texts[start : start + batch_size]
        encoded = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        encoded = {key: value.to(device) for key, value in encoded.items()}
        logits = model(**encoded).logits
        probs = F.softmax(logits, dim=-1)
        scores, pred_ids = probs.max(dim=-1)
        for text, pred_id, score in zip(
            batch_texts,
            pred_ids.tolist(),
            scores.tolist(),
            strict=True,
        ):
            raw_label = id2label.get(int(pred_id), f"label_{pred_id}")
            sentiment = normalize_binary_sentiment(raw_label, positive_labels, negative_labels)
            rows.append(
                {
                    "text": text,
                    "sentiment": sentiment,
                    "sentiment_id": 1 if sentiment == "positive" else 0 if sentiment else None,
                    "sentiment_score": float(score),
                    "raw_sentiment_label": raw_label,
                    "source": "airbnb_pseudo_label",
                }
            )
    return pd.DataFrame(rows, columns=columns)


def _balanced_sample(
    data: pd.DataFrame,
    max_per_class: int | None,
    seed: int,
) -> pd.DataFrame:
    counts = data["sentiment"].value_counts()
    if counts.empty:
        return data
    per_class = int(counts.min())
    if max_per_class:
        per_class = min(per_class, int(max_per_class))
    sampled = [
        frame.sample(min(len(frame), per_class), random_state=seed)
        for _, frame in data.groupby("sentiment", sort=False)
    ]
    return pd.concat(sampled, ignore_index=True)


def _sample_for_labeling(
    reviews: pd.DataFrame,
    max_reviews: int | str | None,
    seed: int,
) -> pd.DataFrame:
    if max_reviews:
        return reviews.sample(
            min(len(reviews), int(max_reviews)),
            random_state=seed,
        ).reset_index(drop=True)
    return reviews.reset_index(drop=True)


def _label_reviews_dataframe(cfg: dict, reviews_for_labeling: pd.DataFrame) -> pd.DataFrame:
    if reviews_for_labeling.empty:
        predictions = predict_binary_sentiment(
            [],
            model_name=cfg_get(cfg, "sentiment_labeling.model_name"),
            batch_size=int(cfg_get(cfg, "sentiment_labeling.batch_size")),
            max_length=int(cfg_get(cfg, "sentiment_labeling.max_length")),
            positive_labels=cfg_get(cfg, "sentiment_labeling.positive_labels"),
            negative_labels=cfg_get(cfg, "sentiment_labeling.negative_labels"),
        )
    else:
        predictions = predict_binary_sentiment(
            reviews_for_labeling["comments_clean"].tolist(),
            model_name=cfg_get(cfg, "sentiment_labeling.model_name"),
            batch_size=int(cfg_get(cfg, "sentiment_labeling.batch_size")),
            max_length=int(cfg_get(cfg, "sentiment_labeling.max_length")),
            positive_labels=cfg_get(cfg, "sentiment_labeling.positive_labels"),
            negative_labels=cfg_get(cfg, "sentiment_labeling.negative_labels"),
        )

    return pd.concat(
        [
            reviews_for_labeling[
                [
                    col
                    for col in ["id", "listing_id", "date", "comments_clean"]
                    if col in reviews_for_labeling.columns
                ]
            ].reset_index(drop=True),
            predictions.drop(columns=["text"]).reset_index(drop=True),
        ],
        axis=1,
    )


def _make_high_confidence_dataset(
    labeled: pd.DataFrame,
    threshold: float,
    balance_classes: bool,
    max_per_class: int | str | None,
    seed: int,
) -> pd.DataFrame:
    train_data = labeled[
        labeled["sentiment"].isin(["negative", "positive"])
        & (labeled["sentiment_score"] >= threshold)
    ].copy()
    train_data = train_data.rename(columns={"comments_clean": "text"})
    if train_data.empty:
        return pd.DataFrame(
            columns=[
                "text",
                "sentiment",
                "label_id",
                "sentiment_score",
                "raw_sentiment_label",
                "source",
            ]
        )
    train_data["label_id"] = train_data["sentiment_id"].astype(int)
    train_data = train_data.drop_duplicates(subset=["text"])

    if balance_classes:
        train_data = _balanced_sample(train_data, max_per_class, seed)

    return train_data


def _label_split(
    cfg: dict,
    reviews_path,
    max_reviews: int | str | None,
    output_path,
    high_confidence_path,
    balance_classes: bool,
    max_per_class: int | str | None,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    reviews = pd.read_parquet(reviews_path)
    reviews_for_labeling = _sample_for_labeling(reviews, max_reviews, seed)
    labeled = _label_reviews_dataframe(cfg, reviews_for_labeling)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    labeled.to_parquet(output_path, index=False)

    threshold = float(cfg_get(cfg, "sentiment_labeling.min_confidence"))
    high_confidence = _make_high_confidence_dataset(
        labeled,
        threshold,
        balance_classes,
        max_per_class,
        seed,
    )
    high_confidence_path.parent.mkdir(parents=True, exist_ok=True)
    high_confidence[
        [
            "text",
            "sentiment",
            "label_id",
            "sentiment_score",
            "raw_sentiment_label",
            "source",
        ]
    ].to_parquet(high_confidence_path, index=False)
    return labeled, high_confidence


def _split_report(
    input_path,
    labeled: pd.DataFrame,
    high_confidence: pd.DataFrame,
    threshold: float,
) -> dict[str, Any]:
    return {
        "input_reviews_path": str(input_path),
        "input_rows": int(len(labeled)),
        "full_labeled_rows": int(len(labeled)),
        "min_confidence": threshold,
        "high_confidence_rows": int(len(high_confidence)),
        "raw_label_counts": labeled["raw_sentiment_label"].value_counts().to_dict()
        if "raw_sentiment_label" in labeled
        else {},
        "sentiment_counts": labeled["sentiment"].value_counts().to_dict()
        if "sentiment" in labeled
        else {},
        "high_confidence_sentiment_counts": high_confidence["sentiment"].value_counts().to_dict()
        if "sentiment" in high_confidence
        else {},
        "high_confidence_score_mean": float(high_confidence["sentiment_score"].mean())
        if len(high_confidence)
        else None,
    }


def label_airbnb_sentiment(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    seed = int(cfg_get(cfg, "experiment.seed"))
    threshold = float(cfg_get(cfg, "sentiment_labeling.min_confidence"))

    train_labeled, train_data = _label_split(
        cfg,
        files["airbnb_reviews_finetune_window"],
        cfg_get(cfg, "sentiment_labeling.max_labeled_reviews"),
        files["airbnb_reviews_finetune_sentiment"],
        files["teacher_reviews"],
        bool(cfg_get(cfg, "sentiment_labeling.balance_classes")),
        cfg_get(cfg, "sentiment_labeling.max_per_class"),
        seed,
    )

    eval_labeled, eval_data = _label_split(
        cfg,
        files["airbnb_reviews_sentiment_eval_window"],
        cfg_get(cfg, "sentiment_labeling.max_eval_labeled_reviews"),
        files["airbnb_reviews_sentiment_eval"],
        files["sentiment_eval_reviews"],
        bool(cfg_get(cfg, "sentiment_labeling.balance_eval_classes")),
        cfg_get(cfg, "sentiment_labeling.max_eval_per_class"),
        seed,
    )

    report = {
        "labeling_model": cfg_get(cfg, "sentiment_labeling.model_name"),
        "train": _split_report(
            files["airbnb_reviews_finetune_window"],
            train_labeled,
            train_data,
            threshold,
        ),
        "eval": _split_report(
            files["airbnb_reviews_sentiment_eval_window"],
            eval_labeled,
            eval_data,
            threshold,
        ),
    }
    write_json(report, paths["reports_dir"] / "airbnb_sentiment_labeling.json")
    return {
        "finetune_sentiment": str(files["airbnb_reviews_finetune_sentiment"]),
        "sentiment_eval": str(files["airbnb_reviews_sentiment_eval"]),
        "teacher_reviews": str(files["teacher_reviews"]),
        "sentiment_eval_reviews": str(files["sentiment_eval_reviews"]),
    }
