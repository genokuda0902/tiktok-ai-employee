import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from render import SCENES
def test_three_scenes(): assert len(SCENES)==3
def test_caption_readable(): assert all(0<len(s[2])<=20 for s in SCENES)
def test_no_sensitive_assets(): assert all("IMG_" not in str(s) for s in SCENES)
