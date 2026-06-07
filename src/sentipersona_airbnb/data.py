from __future__ import annotations

import html
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .config import cfg_get, standard_files, standard_paths
from .utils import require_columns, write_json

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b\S+@\S+\.\S+\b")
PHONE_RE = re.compile(r"\+?\d[\d\s\-().]{7,}\d")
SPACE_RE = re.compile(r"\s+")


def clean_review(text: Any) -> str | None:
    if not isinstance(text, str):
        return None
    text = html.unescape(text).strip()
    if not text:
        return None
    text = URL_RE.sub("", text)
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = SPACE_RE.sub(" ", text).strip()
    return text or None


def load_fasttext_model(model_path: Path):
    try:
        import fasttext
    except ImportError as exc:
        raise RuntimeError("Install optional dependency: pip install -e .[fasttext]") from exc
    return fasttext.load_model(str(model_path))


def filter_language_fasttext(
    texts: pd.Series,
    target_language: str | None,
    model_path: Path | None,
    threshold: float,
    strict: bool,
) -> pd.Series:
    if not target_language:
        return pd.Series(True, index=texts.index)
    if model_path is None or not model_path.exists():
        if strict:
            raise FileNotFoundError(
                f"Language filter requested for {target_language!r}, but {model_path} is missing."
            )
        return pd.Series(True, index=texts.index)

    try:
        model = load_fasttext_model(model_path)
    except RuntimeError:
        if strict:
            raise
        return pd.Series(True, index=texts.index)

    def is_target(text: str) -> bool:
        labels, probs = model.predict(text.replace("\n", " "), k=1)
        detected = labels[0].replace("__label__", "")
        return detected == target_language and probs[0] >= threshold

    return texts.map(is_target)


def latest_inside_airbnb_dir(cfg: dict) -> Path:
    root = standard_paths(cfg)["inside_airbnb_dir"]
    manifests = sorted(root.glob("*/manifest.json"))
    if manifests:
        return manifests[-1].parent
    snapshots = sorted([path for path in root.glob("*") if path.is_dir()])
    if snapshots:
        return snapshots[-1]
    raise FileNotFoundError(f"No Inside Airbnb snapshot found under {root}")


def filter_reviews_by_recent_months(
    reviews: pd.DataFrame,
    months: int | str | None,
    end: str | None = "latest",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    report: dict[str, Any] = {
        "enabled": False,
        "months": None,
        "end": end,
        "start_month": None,
        "end_month": None,
        "rows_before": int(len(reviews)),
        "rows_after": int(len(reviews)),
    }
    if months in (None, "", 0, "0"):
        return reviews, report

    months_int = int(months)
    if months_int < 1:
        raise ValueError("Review window months must be null or a positive integer.")

    dates = pd.to_datetime(reviews["date"], errors="coerce")
    valid_dates = dates.notna()
    report["enabled"] = True
    report["months"] = months_int
    if not valid_dates.any():
        report["rows_after"] = 0
        return reviews.iloc[0:0].copy(), report

    periods = dates.dt.to_period("M")
    if end is None or str(end).strip().lower() == "latest":
        end_period = periods[valid_dates].max()
    else:
        end_period = pd.Period(str(end)[:7], freq="M")
    start_period = end_period - (months_int - 1)

    mask = valid_dates & (periods >= start_period) & (periods <= end_period)
    filtered = reviews[mask].copy()
    report.update(
        {
            "start_month": str(start_period),
            "end_month": str(end_period),
            "rows_after": int(len(filtered)),
        }
    )
    return filtered, report


def filter_reviews_for_eval_window(
    reviews: pd.DataFrame,
    months: int | str | None,
    end: str | None,
    finetune_window_report: dict[str, Any],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    if end and str(end).strip().lower() == "before_finetune":
        start_month = finetune_window_report.get("start_month")
        if start_month is None:
            return filter_reviews_by_recent_months(reviews, months, None)
        end_period = pd.Period(start_month, freq="M") - 1
        return filter_reviews_by_recent_months(reviews, months, str(end_period))
    return filter_reviews_by_recent_months(reviews, months, end)


def preprocess_inside_airbnb(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    snapshot_dir = latest_inside_airbnb_dir(cfg)
    reviews_path = snapshot_dir / "reviews.csv.gz"
    listings_path = snapshot_dir / "listings.csv.gz"
    calendar_path = snapshot_dir / "calendar.csv.gz"

    reviews = pd.read_csv(reviews_path)
    require_columns(reviews.columns, ["listing_id", "id", "date", "comments"], "reviews.csv.gz")
    reviews["comments_clean"] = reviews["comments"].map(clean_review)
    reviews = reviews.dropna(subset=["comments_clean"]).copy()
    cleaned_rows = int(len(reviews))

    reviews["date"] = pd.to_datetime(reviews["date"], errors="coerce")
    reviews = reviews.dropna(subset=["date"])

    before_language_rows = int(len(reviews))
    target_language = cfg_get(cfg, "data.target_language")
    language_model = paths["language_model_dir"] / "lid.176.bin"
    mask = filter_language_fasttext(
        reviews["comments_clean"],
        target_language,
        language_model,
        float(cfg_get(cfg, "data.language_threshold")),
        bool(cfg_get(cfg, "data.strict_language_filter")),
    )
    reviews = reviews[mask].copy()

    before_sampling_rows = int(len(reviews))
    max_reviews = cfg_get(cfg, "data.max_airbnb_reviews")
    if max_reviews:
        reviews = reviews.sample(min(len(reviews), int(max_reviews)), random_state=42)

    finetune_window, finetune_window_report = filter_reviews_by_recent_months(
        reviews,
        cfg_get(
            cfg,
            "data.finetune_review_window_months",
            cfg_get(cfg, "data.review_window_months"),
        ),
        cfg_get(
            cfg,
            "data.finetune_review_window_end",
            cfg_get(cfg, "data.review_window_end", "latest"),
        ),
    )
    sentiment_eval_window, sentiment_eval_window_report = filter_reviews_for_eval_window(
        reviews,
        cfg_get(cfg, "data.sentiment_eval_review_window_months"),
        cfg_get(cfg, "data.sentiment_eval_review_window_end", "before_finetune"),
        finetune_window_report,
    )

    listings = pd.read_csv(listings_path)
    require_columns(listings.columns, ["id"], "listings.csv.gz")
    listing_keep = [
        col
        for col in [
            "id",
            "neighbourhood_cleansed",
            "room_type",
            "price",
            "availability_365",
            "number_of_reviews_ltm",
            "review_scores_rating",
            "review_scores_cleanliness",
            "review_scores_location",
            "review_scores_value",
            "minimum_nights",
        ]
        if col in listings.columns
    ]
    listings_small = listings[listing_keep].rename(columns={"id": "listing_id"})
    reviews = reviews.merge(listings_small, on="listing_id", how="left")
    finetune_window = finetune_window.merge(listings_small, on="listing_id", how="left")
    sentiment_eval_window = sentiment_eval_window.merge(listings_small, on="listing_id", how="left")

    calendar_occ = compute_monthly_calendar_occupancy(calendar_path)
    review_occ = estimate_review_based_occupancy(
        reviews,
        listings_small,
        review_rate=float(cfg_get(cfg, "occupancy.review_rate")),
        default_length_of_stay=float(cfg_get(cfg, "occupancy.default_length_of_stay")),
        cap=float(cfg_get(cfg, "occupancy.cap_review_based_occupancy")),
    )

    processed_reviews = files["airbnb_reviews_all"]
    legacy_reviews = files["airbnb_reviews_legacy"]
    finetune_reviews = files["airbnb_reviews_finetune_window"]
    sentiment_eval_reviews = files["airbnb_reviews_sentiment_eval_window"]
    monthly_occ = files["monthly_occupancy"]
    review_occ_path = files["review_based_occupancy"]
    processed_reviews.parent.mkdir(parents=True, exist_ok=True)
    reviews.to_parquet(processed_reviews, index=False)
    reviews.to_parquet(legacy_reviews, index=False)
    finetune_window.to_parquet(finetune_reviews, index=False)
    sentiment_eval_window.to_parquet(sentiment_eval_reviews, index=False)
    calendar_occ.to_parquet(monthly_occ, index=False)
    review_occ.to_parquet(review_occ_path, index=False)

    quality = {
        "snapshot_dir": str(snapshot_dir),
        "reviews_after_cleaning": cleaned_rows,
        "production_review_scope": "all_clean_language_filtered_reviews",
        "finetune_review_window": finetune_window_report,
        "sentiment_eval_review_window": sentiment_eval_window_report,
        "reviews_before_language_filter": before_language_rows,
        "reviews_before_max_review_sampling": before_sampling_rows,
        "production_reviews_clean_rows": int(len(reviews)),
        "production_reviews_listing_count": int(reviews["listing_id"].nunique()),
        "finetune_reviews_clean_rows": int(len(finetune_window)),
        "finetune_reviews_listing_count": int(finetune_window["listing_id"].nunique()),
        "sentiment_eval_reviews_clean_rows": int(len(sentiment_eval_window)),
        "sentiment_eval_reviews_listing_count": int(
            sentiment_eval_window["listing_id"].nunique()
        ),
        "language_filter": target_language,
        "calendar_monthly_rows": int(len(calendar_occ)),
        "review_based_occupancy_rows": int(len(review_occ)),
    }
    write_json(quality, paths["reports_dir"] / "airbnb_data_quality.json")
    return {
        "reviews_all": str(processed_reviews),
        "reviews_legacy": str(legacy_reviews),
        "reviews_finetune_window": str(finetune_reviews),
        "reviews_sentiment_eval_window": str(sentiment_eval_reviews),
        "monthly_occupancy": str(monthly_occ),
        "review_based_occupancy": str(review_occ_path),
    }


def compute_monthly_calendar_occupancy(calendar_path: Path) -> pd.DataFrame:
    usecols = ["listing_id", "date", "available"]
    calendar = pd.read_csv(calendar_path, usecols=usecols)
    require_columns(calendar.columns, usecols, "calendar.csv.gz")
    calendar["date"] = pd.to_datetime(calendar["date"], errors="coerce")
    calendar = calendar.dropna(subset=["date"])
    calendar["year_month"] = calendar["date"].dt.to_period("M").astype(str)
    calendar["is_unavailable"] = calendar["available"].astype(str).str.lower().eq("f")
    grouped = (
        calendar.groupby(["listing_id", "year_month"], as_index=False)
        .agg(occupancy_rate=("is_unavailable", "mean"), calendar_days=("is_unavailable", "size"))
        .sort_values(["listing_id", "year_month"])
    )
    return grouped


def estimate_review_based_occupancy(
    reviews: pd.DataFrame,
    listings: pd.DataFrame,
    review_rate: float = 0.50,
    default_length_of_stay: float = 3.0,
    cap: float = 0.70,
) -> pd.DataFrame:
    if reviews.empty:
        return pd.DataFrame(
            columns=["listing_id", "year_month", "review_count", "review_based_occupancy"]
        )
    data = reviews[["listing_id", "date"]].copy()
    data["year_month"] = pd.to_datetime(data["date"]).dt.to_period("M")
    monthly = data.groupby(["listing_id", "year_month"]).size().reset_index(name="review_count")
    if "minimum_nights" in listings.columns:
        minimum_nights = listings[["listing_id", "minimum_nights"]].copy()
    else:
        minimum_nights = listings[["listing_id"]].copy()
        minimum_nights["minimum_nights"] = default_length_of_stay
    monthly = monthly.merge(minimum_nights, on="listing_id", how="left")
    monthly["length_of_stay"] = np.maximum(
        monthly["minimum_nights"].fillna(default_length_of_stay).astype(float),
        default_length_of_stay,
    )
    monthly["days_in_month"] = monthly["year_month"].map(lambda p: p.days_in_month)
    monthly["est_booked_nights"] = (
        monthly["review_count"] / max(review_rate, 1e-6) * monthly["length_of_stay"]
    )
    monthly["review_based_occupancy"] = (
        monthly["est_booked_nights"] / monthly["days_in_month"]
    ).clip(0, cap)
    monthly["year_month"] = monthly["year_month"].astype(str)
    return monthly.drop(columns=["minimum_nights"])


def validate_occupancy_proxy(
    calendar_occ: pd.DataFrame,
    review_occ: pd.DataFrame,
    min_r: float = 0.60,
) -> dict[str, Any]:
    merged = calendar_occ.merge(
        review_occ[["listing_id", "year_month", "review_based_occupancy"]],
        on=["listing_id", "year_month"],
        how="inner",
    ).dropna()
    if len(merged) < 3:
        return {"n": int(len(merged)), "pearson_r": math.nan, "passed": False}
    from scipy import stats

    r, p = stats.pearsonr(merged["occupancy_rate"], merged["review_based_occupancy"])
    return {
        "n": int(len(merged)),
        "pearson_r": float(r),
        "p_value": float(p),
        "passed": bool(r >= min_r),
    }
