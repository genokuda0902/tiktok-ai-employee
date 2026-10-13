"""Contract tests for cycle543 lighting. Run with python -m pytest -q."""
from pathlib import Path
import numpy as np
from PIL import Image
from cinematic_lighting import GENRES,TIMES,W,H,make_light_map

def test_ten_genres():
    assert len(GENRES)==10

def test_timeline():
    assert len(TIMES)==9 and TIMES[0]==0 and TIMES[-1]==12.5
    assert all(b>a for a,b in zip(TIMES,TIMES[1:]))

def test_palette():
    assert all(len(c)==3 and all(0<=v<=255 for v in c) for c in GENRES.values())

def test_safe_text_regions(tmp_path):
    for scene in range(8):
        path=tmp_path/f"light_{scene}.png"
        stats=make_light_map(scene,GENRES["雑学・科学"],path)
        img=np.asarray(Image.open(path).convert("RGBA"))
        assert img.shape==(H,W,4)
        assert img[:565,:,3].max()==0
        assert img[1360:,:,3].max()==0
        assert img[600:1300,:,3].max()>35
        assert stats["max_top_alpha"]==0 and stats["max_bottom_alpha"]==0
