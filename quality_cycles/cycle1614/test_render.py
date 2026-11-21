from pathlib import Path
import ast
from render import SCENES
def test_three_scenes(): assert len(SCENES)==3
def test_all_japanese(): assert all(any(ord(c)>127 for c in scene[0]) for scene in SCENES)
def test_no_private_assets(): assert "IMG_5805" not in Path(__file__).with_name("render.py").read_text()
def test_silent_review_only(): assert "REVIEW ONLY" in Path(__file__).with_name("render.py").read_text()
