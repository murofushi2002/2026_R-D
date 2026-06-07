import numpy as np
import pandas as pd

from sentipersona_airbnb.timeseries import (
    build_analysis_dataset,
    choose_occupancy_source,
    compute_monthly_persona_ratios,
)
from sentipersona_airbnb.utils import write_json


def test_compute_monthly_persona_ratios_excludes_noise_denominator() -> None:
    reviews = pd.DataFrame(
        {
            "listing_id": [1, 1, 1],
            "date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03"]),
        }
    )
    labels = np.array([0, 1, -1])
    probabilities = np.array([0.5, 0.5, 1.0])
    out = compute_monthly_persona_ratios(reviews, labels, probabilities)
    assert out.loc[0, "persona_0_ratio"] == 0.5
    assert out.loc[0, "persona_1_ratio"] == 0.5
    assert out.loc[0, "noise_ratio"] == 1 / 3


def test_build_analysis_dataset_applies_review_lag() -> None:
    persona = pd.DataFrame(
        {
            "listing_id": [1],
            "year_month": ["2026-02"],
            "review_count": [10],
            "noise_ratio": [0.0],
            "persona_0_ratio": [1.0],
        }
    )
    occupancy = pd.DataFrame(
        {"listing_id": [1], "year_month": ["2026-01"], "occupancy_rate": [0.8]}
    )
    out = build_analysis_dataset(persona, occupancy, lag_months=1)
    assert len(out) == 1
    assert out.loc[0, "analysis_month"] == "2026-01"
    assert out.loc[0, "occupancy_rate"] == 0.8


def test_choose_occupancy_source_auto_falls_back_to_review_based(tmp_path) -> None:
    processed = tmp_path / "processed"
    reports = tmp_path / "reports"
    processed.mkdir()
    reports.mkdir()
    pd.DataFrame(
        {"listing_id": [1], "year_month": ["2026-01"], "review_based_occupancy": [0.4]}
    ).to_parquet(processed / "review_based_occupancy.parquet", index=False)
    write_json({"passed": False}, reports / "occupancy_proxy_validation.json")
    cfg = {
        "paths": {
            "raw_dir": str(tmp_path / "raw"),
            "interim_dir": str(tmp_path / "interim"),
            "processed_dir": str(processed),
            "models_dir": str(tmp_path / "models"),
            "reports_dir": str(reports),
            "artifacts_dir": str(tmp_path / "artifacts"),
        },
        "data": {"city_slug": "test"},
        "experiment": {"name": "test"},
        "training": {"output_subdir": "senticse"},
        "occupancy": {"source": "auto"},
    }
    source, data = choose_occupancy_source(cfg)
    assert source == "review_based"
    assert data.loc[0, "occupancy_rate"] == 0.4
