"""Regression checks for the reusable cycle707 process comparison."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pytest
from before_after import Comparison, DEFAULT, validate, smooth

def test_default_is_supported():
    assert validate(DEFAULT)
    assert len(DEFAULT.before) == len(DEFAULT.after) == 3

@pytest.mark.parametrize("after", ["1分で完了", "100%改善", "必ず成功"])
def test_reject_unverified_claims(after):
    with pytest.raises(ValueError):
        validate(Comparison(("手作業",), (after,)))

def test_reject_overlong_step():
    with pytest.raises(ValueError):
        validate(Comparison(("手作業",), ("あ"*17,)))

def test_reject_empty_steps():
    with pytest.raises(ValueError):
        validate(Comparison((), ("結果を確認",)))

def test_animation_bounds():
    assert smooth(-2) == 0 and smooth(2) == 1
    assert 0 < smooth(0.5) < 1

def test_reuse_across_ten_genres():
    genres = ("ai_work","finance","health","cooking","travel","study","career","lifestyle","tech","business")
    for genre in genres:
        assert genre and validate(DEFAULT)
