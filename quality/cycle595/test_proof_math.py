from proof_math import verified_total

def test_four_values():
    assert verified_total([120,150,200,250]) == 720

def test_partial():
    assert verified_total([120,150]) == 270
