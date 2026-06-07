from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "experiment": {"name": "sentipersona_airbnb", "seed": 42},
    "paths": {
        "raw_dir": "data/raw",
        "interim_dir": "data/interim",
        "processed_dir": "data/processed",
        "models_dir": "models",
        "reports_dir": "reports",
        "artifacts_dir": "artifacts",
    },
    "data": {
        "target_city": "Tokyo",
        "city_slug": "tokyo",
        "inside_airbnb_page": "https://insideairbnb.com/get-the-data/",
        "inside_airbnb_snapshot": "latest",
        "inside_airbnb_files": ["listings.csv.gz", "reviews.csv.gz", "calendar.csv.gz"],
        "target_language": "en",
        "language_threshold": 0.80,
        "strict_language_filter": False,
        "finetune_review_window_months": 3,
        "finetune_review_window_end": "latest",
        "sentiment_eval_review_window_months": 3,
        "sentiment_eval_review_window_end": "before_finetune",
        "max_airbnb_reviews": None,
    },
    "sentiment_labeling": {
        "model_name": "models/finetune",
        "batch_size": 64,
        "max_length": 256,
        "min_confidence": 0.95,
        "max_labeled_reviews": None,
        "max_eval_labeled_reviews": None,
        "balance_classes": True,
        "max_per_class": None,
        "balance_eval_classes": True,
        "max_eval_per_class": None,
        "positive_labels": ["positive", "pos", "label_1"],
        "negative_labels": ["negative", "neg", "label_0"],
    },
    "occupancy": {
        "source": "auto",
        "review_rate": 0.50,
        "default_length_of_stay": 3.0,
        "cap_review_based_occupancy": 0.70,
        "min_calendar_review_correlation": 0.60,
    },
    "training": {
        "base_model": "models/sentense",
        "output_subdir": "senticse",
        "batch_size": 32,
        "epochs": 5,
        "learning_rate": 2e-5,
        "temperature": 0.07,
        "max_length": 256,
        "max_train_samples": None,
        "eval_samples_per_class": 1000,
        "mixed_precision": True,
    },
    "model_evaluation": {"max_samples_per_class": 1000},
    "embedding": {"batch_size": 256, "normalize": True},
    "clustering": {
        "n_components_cluster": 50,
        "n_components_vis": 2,
        "n_neighbors": 15,
        "deterministic_umap": False,
        "n_jobs": -1,
        "fit_separate_visual_umap": False,
        "min_dist_cluster": 0.0,
        "min_dist_vis": 0.1,
        "min_cluster_size_ratio": 0.02,
        "min_samples": 5,
        "metric_sample_size": 10000,
        "representative_reviews_per_cluster": 12,
    },
    "persona": {
        "ollama_model": "qwen3:4b",
        "output_language": "Japanese",
        "repetitions": 3,
        "temperature": 0.0,
        "timeout_seconds": 120,
    },
    "timeseries": {"lag_months": 1, "min_monthly_reviews": 5, "smoothing_window": 3},
    "evaluation": {
        "sgts_min_delta": 0.40,
        "silhouette_min": 0.30,
        "noise_ratio_max": 0.20,
        "persona_name_consistency_min": 0.70,
        "occupancy_abs_corr_min": 0.30,
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    if path is None:
        return deepcopy(DEFAULT_CONFIG)
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    cfg = deep_merge(DEFAULT_CONFIG, loaded)
    cfg["_config_path"] = str(path)
    return cfg


def cfg_get(cfg: dict[str, Any], dotted_key: str, default: Any = None) -> Any:
    node: Any = cfg
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def project_path(cfg: dict[str, Any], dotted_key: str) -> Path:
    value = cfg_get(cfg, dotted_key)
    if value is None:
        raise KeyError(f"Missing path config: {dotted_key}")
    return Path(value)


def standard_paths(cfg: dict[str, Any]) -> dict[str, Path]:
    paths = {name: Path(value) for name, value in cfg["paths"].items()}
    raw = paths["raw_dir"]
    city_slug = cfg_get(cfg, "data.city_slug", "city")
    exp_name = cfg_get(cfg, "experiment.name", "experiment")
    paths["inside_airbnb_dir"] = raw / "inside_airbnb" / city_slug
    paths["language_model_dir"] = paths["models_dir"] / "language"
    paths["senticse_model_dir"] = paths["models_dir"] / cfg_get(
        cfg, "training.output_subdir", "senticse"
    ) / exp_name
    return paths


def standard_files(cfg: dict[str, Any]) -> dict[str, Path]:
    paths = standard_paths(cfg)
    return {
        "airbnb_reviews_all": paths["processed_dir"] / "airbnb_reviews_clean_all.parquet",
        "airbnb_reviews_legacy": paths["processed_dir"] / "airbnb_reviews_clean.parquet",
        "airbnb_reviews_finetune_window": paths["processed_dir"]
        / "airbnb_reviews_finetune_window.parquet",
        "airbnb_reviews_sentiment_eval_window": paths["processed_dir"]
        / "airbnb_reviews_sentiment_eval_window.parquet",
        "airbnb_reviews_finetune_sentiment": paths["processed_dir"]
        / "airbnb_reviews_finetune_sentiment.parquet",
        "airbnb_reviews_sentiment_eval": paths["processed_dir"]
        / "airbnb_reviews_sentiment_eval.parquet",
        "monthly_occupancy": paths["processed_dir"] / "monthly_occupancy.parquet",
        "review_based_occupancy": paths["processed_dir"] / "review_based_occupancy.parquet",
        "teacher_reviews": paths["interim_dir"] / "teacher_reviews.parquet",
        "sentiment_eval_reviews": paths["interim_dir"] / "sentiment_eval_reviews.parquet",
        "airbnb_review_embeddings": paths["processed_dir"] / "airbnb_review_embeddings.npy",
        "regional_cluster_labels": paths["processed_dir"] / "regional_cluster_labels.npy",
        "regional_cluster_probabilities": paths["processed_dir"]
        / "regional_cluster_probabilities.npy",
    }
