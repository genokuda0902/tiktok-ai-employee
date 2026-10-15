import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_cycle603 import REGION, FPS, FRAME_COUNT, accent_for, draw_cue

def test_10_genres():
    import json
    config=json.loads((Path(__file__).resolve().parents[1]/"assets/genres.json").read_text())
    assert len(config["genres"])==10
    for genre in config["genres"]: assert len(accent_for(genre))==3

def test_fade_and_safe_zone():
    assert FPS==30 and FRAME_COUNT==54
    x,y,w,h=REGION
    assert 100<x<x+w<900 and 400<y<y+h<950
    theme=accent_for("雑学・科学")
    assert draw_cue(0,theme).getbbox() is None
    assert draw_cue(27,theme).getbbox() is not None
    assert draw_cue(53,theme).getbbox() is None
