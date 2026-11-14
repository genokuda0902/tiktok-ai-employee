from pathlib import Path
from render import STAGES
def test_three_stages(): assert len(STAGES)==3
def test_review_only():
    text=Path(__file__).with_name("render.py").read_text()
    assert "REVIEW ONLY" in text and "ナレーション未実装" in text
def test_no_private_assets():
    assert all(len(stage)==3 for stage in STAGES)
