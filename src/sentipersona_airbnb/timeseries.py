from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .config import cfg_get, standard_files, standard_paths
from .utils import read_json, write_json


def compute_monthly_persona_ratios(
    reviews: pd.DataFrame,
    labels: np.ndarray,
    probabilities: np.ndarray | None = None,
) -> pd.DataFrame:
    if len(reviews) != len(labels):
        raise ValueError("reviews and labels length mismatch")
    data = reviews[["listing_id", "date"]].copy()
    data["year_month"] = pd.to_datetime(data["date"]).dt.to_period("M").astype(str)
    data["cluster"] = labels
    data["cluster_probability"] = probabilities if probabilities is not None else 1.0
    valid = data["cluster"] != -1
    persona_ids = sorted(int(x) for x in set(data.loc[valid, "cluster"]))

    monthly = []
    for (listing_id, year_month), group in data.groupby(["listing_id", "year_month"]):
        record: dict[str, Any] = {
            "listing_id": listing_id,
            "year_month": year_month,
            "review_count": int(len(group)),
            "noise_ratio": float((group["cluster"] == -1).mean()),
        }
        denom = max(float(group.loc[group["cluster"] != -1, "cluster_probability"].sum()), 1e-12)
        for persona_id in persona_ids:
            mask = group["cluster"] == persona_id
            record[f"persona_{persona_id}_ratio"] = float(
                group.loc[mask, "cluster_probability"].sum() / denom
            )
        monthly.append(record)
    return pd.DataFrame(monthly).sort_values(["listing_id", "year_month"])


def smooth_persona_ratios(df: pd.DataFrame, window: int, min_reviews: int) -> pd.DataFrame:
    if df.empty:
        return df
    persona_cols = [col for col in df.columns if col.startswith("persona_")]
    out = df.copy()
    out["reliable"] = out["review_count"] >= min_reviews
    for col in persona_cols:
        smoothed = []
        for _listing_id, group in out.groupby("listing_id"):
            weights = group["review_count"].clip(lower=1).astype(float)
            numerator = (group[col] * weights).rolling(window, min_periods=1, center=True).sum()
            denominator = weights.rolling(window, min_periods=1, center=True).sum()
            smoothed.extend((numerator / denominator).tolist())
        out[f"{col}_smoothed"] = smoothed
    return out


def build_analysis_dataset(
    persona_monthly: pd.DataFrame,
    occupancy_monthly: pd.DataFrame,
    lag_months: int,
) -> pd.DataFrame:
    persona = persona_monthly.copy()
    period = pd.PeriodIndex(persona["year_month"], freq="M") - lag_months
    persona["analysis_month"] = period.astype(str)
    occupancy = occupancy_monthly.rename(columns={"year_month": "analysis_month"})
    df = persona.merge(occupancy, on=["listing_id", "analysis_month"], how="inner")
    df["month"] = pd.PeriodIndex(df["analysis_month"], freq="M").month
    for month in range(1, 13):
        df[f"month_{month}"] = (df["month"] == month).astype(int)
    return df.dropna(subset=["occupancy_rate"])


def choose_occupancy_source(cfg: dict) -> tuple[str, pd.DataFrame]:
    paths = standard_paths(cfg)
    requested = cfg_get(cfg, "occupancy.source", "auto")
    validation_path = paths["reports_dir"] / "occupancy_proxy_validation.json"
    if requested == "auto" and validation_path.exists():
        validation = read_json(validation_path)
        requested = "calendar" if validation.get("passed") else "review_based"
    elif requested == "auto":
        requested = "calendar"

    if requested == "review_based":
        data = pd.read_parquet(standard_files(cfg)["review_based_occupancy"])
        data = data.rename(columns={"review_based_occupancy": "occupancy_rate"})
        return "review_based", data[["listing_id", "year_month", "occupancy_rate"]]
    if requested == "calendar":
        data = pd.read_parquet(standard_files(cfg)["monthly_occupancy"])
        return "calendar", data[["listing_id", "year_month", "occupancy_rate"]]
    raise ValueError("occupancy.source must be one of: auto, calendar, review_based")


def run_timeseries(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    files = standard_files(cfg)
    reviews = pd.read_parquet(files["airbnb_reviews_all"])
    labels = np.load(files["regional_cluster_labels"])
    probabilities_path = files["regional_cluster_probabilities"]
    probabilities = np.load(probabilities_path) if probabilities_path.exists() else None
    occupancy_source, occupancy = choose_occupancy_source(cfg)

    monthly = compute_monthly_persona_ratios(reviews, labels, probabilities)
    monthly = smooth_persona_ratios(
        monthly,
        int(cfg_get(cfg, "timeseries.smoothing_window")),
        int(cfg_get(cfg, "timeseries.min_monthly_reviews")),
    )
    analysis = build_analysis_dataset(
        monthly,
        occupancy,
        int(cfg_get(cfg, "timeseries.lag_months")),
    )

    monthly_path = paths["processed_dir"] / "monthly_persona_ratios.parquet"
    analysis_path = paths["processed_dir"] / "analysis_dataset.parquet"
    monthly.to_parquet(monthly_path, index=False)
    analysis.to_parquet(analysis_path, index=False)
    write_json(
        {
            "monthly_persona_rows": int(len(monthly)),
            "analysis_rows": int(len(analysis)),
            "occupancy_source": occupancy_source,
            "listing_count": int(analysis["listing_id"].nunique()) if not analysis.empty else 0,
        },
        paths["reports_dir"] / "timeseries_manifest.json",
    )
    return {"monthly_persona": str(monthly_path), "analysis_dataset": str(analysis_path)}
