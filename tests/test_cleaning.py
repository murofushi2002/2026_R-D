from sentipersona_airbnb.data import clean_review


def test_clean_review_masks_pii_and_removes_url() -> None:
    text = "Great stay at https://example.com. Email me at user@example.com or +1 555 123 4567."
    cleaned = clean_review(text)
    assert cleaned is not None
    assert "https://" not in cleaned
    assert "[EMAIL]" in cleaned
    assert "[PHONE]" in cleaned


def test_clean_review_keeps_short_text() -> None:
    assert clean_review("Great!") == "Great!"


def test_clean_review_does_not_truncate_long_text() -> None:
    text = " ".join(f"word{i}" for i in range(300))
    cleaned = clean_review(text)
    assert cleaned is not None
    assert len(cleaned.split()) == 300
