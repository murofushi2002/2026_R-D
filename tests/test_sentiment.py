from sentipersona_airbnb.sentiment import normalize_binary_sentiment


def test_normalize_binary_sentiment_maps_common_labels() -> None:
    positives = ["positive", "label_1"]
    negatives = ["negative", "label_0"]
    assert normalize_binary_sentiment("POSITIVE", positives, negatives) == "positive"
    assert normalize_binary_sentiment("LABEL_0", positives, negatives) == "negative"
    assert normalize_binary_sentiment("neutral", positives, negatives) is None
