import pandas as pd

from sentipersona_airbnb.modeling import prepare_teacher_dataframe


def test_prepare_teacher_dataframe_uses_binary_label_id(tmp_path) -> None:
    path = tmp_path / "teacher.parquet"
    pd.DataFrame(
        {
            "text": ["good stay", "bad stay", "great host", "dirty room"],
            "label_id": [1, 0, 1, 0],
            "sentiment": ["positive", "negative", "positive", "negative"],
        }
    ).to_parquet(path, index=False)
    out = prepare_teacher_dataframe(path)
    assert sorted(out["label_id"].unique().tolist()) == [0, 1]
    assert set(out["sentiment"]) == {"positive", "negative"}
