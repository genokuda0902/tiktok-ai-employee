from quality.cycle545.evidence_math import check_total

def test_correct_total():
    assert check_total([120,150,200,250],720)

def test_wrong_total():
    assert not check_total([120,150,200,250],719)
