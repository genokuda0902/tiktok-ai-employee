import pytest
from improve import filtergraph

def test_progress_safe_zone():
    f = filtergraph(20)
    assert "y=1662" in f and "872*t/20.000" in f
    assert "color=0x63E6CA" in f

def test_reject_invalid_duration():
    with pytest.raises(ValueError):
        filtergraph(0)
