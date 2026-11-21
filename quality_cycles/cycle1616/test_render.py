from pathlib import Path
from quality_cycles.cycle1616.render import SCENES

def test_three_scenes():
    assert len(SCENES) == 3
    assert all(len(scene)==3 for scene in SCENES)

def test_caption_length():
    assert all(0 < len(scene[2]) <= 22 for scene in SCENES)

def test_review_only():
    source=Path(__file__).with_name("render.py").read_text()
    assert "REVIEW ONLY" in source
    assert "scan_x" in source and "progress" in source
