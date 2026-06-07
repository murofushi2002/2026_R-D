import pandas as pd

from sentipersona_airbnb.config import load_config, standard_files
from sentipersona_airbnb.data import filter_reviews_by_recent_months, preprocess_inside_airbnb


def test_filter_reviews_by_latest_three_calendar_months() -> None:
    reviews = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "date": pd.to_datetime(
                ["2026-01-31", "2026-02-01", "2026-03-15", "2026-04-01", "2026-04-30"]
            ),
        }
    )

    filtered, report = filter_reviews_by_recent_months(reviews, months=3, end="latest")

    assert filtered["id"].tolist() == [2, 3, 4, 5]
    assert report["enabled"] is True
    assert report["start_month"] == "2026-02"
    assert report["end_month"] == "2026-04"


def test_filter_reviews_by_recent_months_can_be_disabled() -> None:
    reviews = pd.DataFrame({"id": [1], "date": pd.to_datetime(["2026-01-01"])})

    filtered, report = filter_reviews_by_recent_months(reviews, months=None)

    assert filtered is reviews
    assert report["enabled"] is False


def test_preprocess_writes_all_reviews_and_finetune_window(tmp_path) -> None:
    snapshot = tmp_path / "raw" / "inside_airbnb" / "testcity" / "2026-04-01"
    snapshot.mkdir(parents=True)
    pd.DataFrame(
        {
            "listing_id": [1, 1, 2, 2],
            "id": [10, 11, 12, 13],
            "date": ["2026-01-01", "2026-02-01", "2026-03-01", "2026-04-01"],
            "comments": [
                "great clean central stay",
                "quiet room near station",
                "bad smell but kind host",
                "excellent location and value",
            ],
        }
    ).to_csv(snapshot / "reviews.csv.gz", index=False, compression="gzip")
    pd.DataFrame(
        {
            "id": [1, 2],
            "minimum_nights": [2, 3],
            "neighbourhood_cleansed": ["A", "B"],
        }
    ).to_csv(snapshot / "listings.csv.gz", index=False, compression="gzip")
    pd.DataFrame(
        {
            "listing_id": [1, 1, 2, 2],
            "date": ["2026-03-01", "2026-03-02", "2026-04-01", "2026-04-02"],
            "available": ["f", "t", "f", "f"],
        }
    ).to_csv(snapshot / "calendar.csv.gz", index=False, compression="gzip")

    cfg = load_config()
    cfg["paths"].update(
        {
            "raw_dir": str(tmp_path / "raw"),
            "interim_dir": str(tmp_path / "interim"),
            "processed_dir": str(tmp_path / "processed"),
            "models_dir": str(tmp_path / "models"),
            "reports_dir": str(tmp_path / "reports"),
            "artifacts_dir": str(tmp_path / "artifacts"),
        }
    )
    cfg["data"].update(
            {
                "city_slug": "testcity",
                "target_language": None,
                "finetune_review_window_months": 2,
                "finetune_review_window_end": "latest",
                "sentiment_eval_review_window_months": 2,
                "sentiment_eval_review_window_end": "before_finetune",
                "max_airbnb_reviews": None,
            }
        )

    preprocess_inside_airbnb(cfg)

    files = standard_files(cfg)
    all_reviews = pd.read_parquet(files["airbnb_reviews_all"])
    finetune_reviews = pd.read_parquet(files["airbnb_reviews_finetune_window"])
    eval_reviews = pd.read_parquet(files["airbnb_reviews_sentiment_eval_window"])

    assert all_reviews["id"].tolist() == [10, 11, 12, 13]
    assert finetune_reviews["id"].tolist() == [12, 13]
    assert eval_reviews["id"].tolist() == [10, 11]
