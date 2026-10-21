from duration_claim import duration_claim


def test_duration_claim():
    assert duration_claim(14.3) == '15秒でわかる'
    assert duration_claim(15.0) == '15秒でわかる'
