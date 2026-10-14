from proof_motion import DEFAULT, GENRES, validate, ease

def test_genres():
    for genre in GENRES:
        assert validate(DEFAULT.__class__(genre, DEFAULT.title, DEFAULT.source_label, DEFAULT.transform_label, DEFAULT.result_label, DEFAULT.values))

def test_total():
    assert sum(DEFAULT.values) == 720

def test_ease():
    assert ease(-1) == 0 and ease(2) == 1
