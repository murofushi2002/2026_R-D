import pandas as pd

from sentipersona_airbnb.data import estimate_review_based_occupancy, validate_occupancy_proxy


def test_estimate_review_based_occupancy_caps_values() -> None:
    reviews = pd.DataFrame(
        {
            "listing_id": [1, 1, 1, 1],
            "date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]),
        }
    )
    listings = pd.DataFrame({"listing_id": [1], "minimum_nights": [30]})
    out = estimate_review_based_occupancy(reviews, listings, review_rate=0.5, cap=0.7)
    assert len(out) == 1
    assert out.loc[0, "review_based_occupancy"] == 0.7


def test_validate_occupancy_proxy() -> None:
    calendar = pd.DataFrame(
        {
            "listing_id": [1, 1, 1],
            "year_month": ["2026-01", "2026-02", "2026-03"],
            "occupancy_rate": [0.2, 0.4, 0.6],
        }
    )
    review = pd.DataFrame(
        {
            "listing_id": [1, 1, 1],
            "year_month": ["2026-01", "2026-02", "2026-03"],
            "review_based_occupancy": [0.1, 0.2, 0.3],
        }
    )
    result = validate_occupancy_proxy(calendar, review, min_r=0.6)
    assert result["passed"] is True
