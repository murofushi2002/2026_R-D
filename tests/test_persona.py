import pytest

from sentipersona_airbnb.persona import persona_prompt, validate_persona


def valid_persona() -> dict:
    return {
        "persona_name": "Transit Comfort Seeker",
        "purpose": "Short city stay near transport",
        "recurring_expressions": [
            {
                "rank": 1,
                "expression": "easy access to train stations",
                "why_recurring": "Several reviews mention train or station access.",
                "evidence_review_ids": ["r1", "r2"],
                "evidence_phrases": ["near the station", "easy train access"],
            }
        ],
        "priorities": [
            {
                "label": "transport access",
                "basis": "Guests repeatedly value station access.",
                "evidence_review_ids": ["r1"],
                "evidence_phrases": ["near the station"],
            }
        ],
        "pain_points": [
            {
                "label": "unknown",
                "basis": "No repeated complaint appears.",
                "evidence_review_ids": [],
                "evidence_phrases": [],
            }
        ],
        "sentiment_tendency": {
            "label": "positive",
            "basis": "Praise dominates the sample.",
            "evidence_review_ids": ["r1"],
        },
        "price_sensitivity": {
            "label": "unknown",
            "basis": "Price is not repeatedly discussed.",
            "evidence_review_ids": [],
        },
        "host_actions": ["Keep directions to the nearest station clear."],
        "confidence": "medium",
        "description": "Guests value convenience and simple access.",
    }


def test_validate_persona_accepts_grounded_schema() -> None:
    assert validate_persona(valid_persona())["confidence"] == "medium"


def test_validate_persona_rejects_invalid_sentiment_label() -> None:
    data = valid_persona()
    data["sentiment_tendency"]["label"] = "neutral"
    with pytest.raises(ValueError, match="sentiment_tendency"):
        validate_persona(data)


def test_persona_prompt_requests_ranked_meaning_expressions() -> None:
    prompt = persona_prompt(
        [
            {
                "review_id": "r1",
                "listing_id": "l1",
                "date": "2025-01-01",
                "text": "The station was very close and check-in was easy.",
            }
        ],
        "Japanese",
    )
    assert "Recurring expressions are not single keywords" in prompt
    assert '"rank": 1' in prompt
    assert "positive|mixed|negative" in prompt
    assert "low|medium|high|unknown" in prompt
    assert "Keep evidence_phrases in the original review language" in prompt
    assert "Do not copy the English placeholder wording" in prompt
