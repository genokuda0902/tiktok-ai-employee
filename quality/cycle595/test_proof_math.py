import pytest
from proof_math import verified_total, caption_safe

def test_four_values():
    assert verified_total([120,150,200,250]) == 720

def test_partial():
    with pytest.raises(ValueError):
        verified_total([120,150])

def test_invalid_type():
    with pytest.raises(ValueError):
        verified_total([120,150,200,True])

def test_caption_safe():
    assert caption_safe(1350,1450)
    assert not caption_safe(1500,1700)
