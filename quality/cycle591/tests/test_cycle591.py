import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_cycle591 import ROOT,SCENES,make_caption

def test_timing():
    assert SCENES[0]["start"]==0
    assert all(a["end"]==b["start"] for a,b in zip(SCENES,SCENES[1:]))
    assert SCENES[-1]["end"]==417

def test_10_genres_render():
    g=json.loads((ROOT/"config/genres.json").read_text(encoding="utf-8"))["genres"]
    assert len(g)==10
    for cfg in g.values():
        assert make_caption(SCENES[0],cfg["theme"]).size==(1080,215)

def test_keyword_and_review():
    assert any("保存して" in s["lines"][-1] for s in SCENES)
    assert "HUMAN_REVIEW" in str(ROOT/"output/cycle591_KEYWORD_CAPTIONS_HUMAN_REVIEW.mp4")
