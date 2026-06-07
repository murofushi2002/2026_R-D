from __future__ import annotations

from itertools import combinations
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

from .config import standard_paths
from .utils import write_json


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(a) * np.linalg.norm(b)), 1e-12)
    return float(np.dot(a, b) / denom)


def sgts_score(
    embeddings: np.ndarray,
    labels: list[str],
    max_pairs: int = 10000,
) -> dict[str, float]:
    if len(embeddings) < 3:
        return {
            "same_sentiment_similarity": float("nan"),
            "different_sentiment_similarity": float("nan"),
            "sgts_delta": float("nan"),
        }
    same = []
    different = []
    for idx, jdx in combinations(range(len(labels)), 2):
        value = _cosine(embeddings[idx], embeddings[jdx])
        if labels[idx] == labels[jdx]:
            same.append(value)
        else:
            different.append(value)
        if len(same) + len(different) >= max_pairs:
            break
    same_mean = float(np.mean(same)) if same else float("nan")
    diff_mean = float(np.mean(different)) if different else float("nan")
    return {
        "same_sentiment_similarity": same_mean,
        "different_sentiment_similarity": diff_mean,
        "sgts_delta": same_mean - diff_mean,
    }


def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    from scipy import stats

    persona_cols = [
        col
        for col in df.columns
        if col.startswith("persona_") and col.endswith(("_ratio", "_smoothed"))
    ]
    rows = []
    for col in persona_cols:
        for lag in [0, 1, 2, 3]:
            shifted = df.groupby("listing_id")[col].shift(lag)
            valid = ~(shifted.isna() | df["occupancy_rate"].isna())
            if valid.sum() < 3:
                continue
            r, p = stats.pearsonr(shifted[valid], df.loc[valid, "occupancy_rate"])
            rows.append(
                {
                    "feature": col,
                    "lag_months": lag,
                    "pearson_r": float(r),
                    "p_value": float(p),
                    "n": int(valid.sum()),
                }
            )
    return pd.DataFrame(rows).sort_values("pearson_r", ascending=False)


def regression_analysis(df: pd.DataFrame) -> dict[str, Any]:
    import statsmodels.api as sm

    persona_cols = [
        col
        for col in df.columns
        if col.startswith("persona_") and col.endswith("_smoothed")
    ]
    if not persona_cols:
        persona_cols = [
            col for col in df.columns if col.startswith("persona_") and col.endswith("_ratio")
        ]
    month_cols = [f"month_{m}" for m in range(2, 13) if f"month_{m}" in df.columns]
    feature_cols = persona_cols + month_cols + ["review_count"]
    data = df.dropna(subset=feature_cols + ["occupancy_rate"])
    if len(data) < len(feature_cols) + 5:
        return {"error": "not enough rows for OLS", "n": int(len(data))}
    x = sm.add_constant(data[feature_cols].astype(float))
    y = data["occupancy_rate"].astype(float)
    model = sm.OLS(y, x).fit(cov_type="HC3")
    return {
        "n": int(len(data)),
        "r2": float(model.rsquared),
        "adj_r2": float(model.rsquared_adj),
        "aic": float(model.aic),
        "coefficients": {key: float(value) for key, value in model.params.items()},
        "p_values": {key: float(value) for key, value in model.pvalues.items()},
    }


def granger_analysis(df: pd.DataFrame, max_lag: int = 3) -> dict[str, Any]:
    from statsmodels.tsa.stattools import grangercausalitytests

    persona_cols = [
        col
        for col in df.columns
        if col.startswith("persona_") and col.endswith("_smoothed")
    ]
    if not persona_cols:
        persona_cols = [
            col for col in df.columns if col.startswith("persona_") and col.endswith("_ratio")
        ]
    regional = df.groupby("analysis_month", as_index=False).agg(
        {"occupancy_rate": "mean", **{col: "mean" for col in persona_cols}}
    )
    regional = regional.sort_values("analysis_month")
    results = {}
    for col in persona_cols:
        data = regional[["occupancy_rate", col]].dropna()
        if len(data) < max_lag + 8:
            continue
        try:
            outcome = grangercausalitytests(data, maxlag=max_lag, verbose=False)
            p_values = {
                str(lag): float(outcome[lag][0]["ssr_ftest"][1]) for lag in range(1, max_lag + 1)
            }
            results[col] = {"min_p_value": min(p_values.values()), "p_values": p_values}
        except Exception as exc:
            results[col] = {"error": str(exc)}
    return results


def xgboost_timeseries_eval(df: pd.DataFrame) -> dict[str, Any]:
    from xgboost import XGBRegressor

    persona_cols = [
        col
        for col in df.columns
        if col.startswith("persona_") and col.endswith(("_ratio", "_smoothed"))
    ]
    month_cols = [f"month_{m}" for m in range(1, 13) if f"month_{m}" in df.columns]
    feature_cols = persona_cols + month_cols + ["review_count", "noise_ratio"]
    data = df.sort_values(["analysis_month", "listing_id"]).dropna(subset=["occupancy_rate"])
    if len(data) < 12:
        return {"error": "not enough rows for XGBoost", "n": int(len(data))}
    x = data[feature_cols].fillna(0).astype(float)
    y = data["occupancy_rate"].astype(float)
    n_splits = min(5, max(2, len(data) // 12))
    splitter = TimeSeriesSplit(n_splits=n_splits)
    rows = []
    for fold, (train_idx, test_idx) in enumerate(splitter.split(x), start=1):
        model = XGBRegressor(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective="reg:squarederror",
        )
        model.fit(x.iloc[train_idx], y.iloc[train_idx])
        pred = model.predict(x.iloc[test_idx])
        rows.append(
            {
                "fold": fold,
                "rmse": float(mean_squared_error(y.iloc[test_idx], pred, squared=False)),
                "mae": float(mean_absolute_error(y.iloc[test_idx], pred)),
                "r2": float(r2_score(y.iloc[test_idx], pred)),
            }
        )
    return {
        "folds": rows,
        "mean_rmse": float(np.mean([row["rmse"] for row in rows])),
        "mean_mae": float(np.mean([row["mae"] for row in rows])),
        "mean_r2": float(np.mean([row["r2"] for row in rows])),
        "feature_count": len(feature_cols),
    }


def run_evaluation(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    analysis_path = paths["processed_dir"] / "analysis_dataset.parquet"
    df = pd.read_parquet(analysis_path)
    corr = correlation_analysis(df)
    corr_path = paths["reports_dir"] / "correlation_results.csv"
    corr.to_csv(corr_path, index=False)
    ols = regression_analysis(df)
    granger = granger_analysis(df)
    xgb = xgboost_timeseries_eval(df)
    summary = {"ols": ols, "granger": granger, "xgboost": xgb}
    summary_path = paths["reports_dir"] / "evaluation_summary.json"
    write_json(summary, summary_path)
    return {"correlation": str(corr_path), "summary": str(summary_path)}
