import json
from pathlib import Path
from hook_engine import make_overlay, W, H, FIRST_SCENE_END, BREAK
ROOT = Path(__file__).resolve().parent
CONF = json.loads((ROOT/'hooks.json').read_text(encoding='utf-8'))

def test_ten_genres():
    assert len(CONF['genres']) == 10
    for name, profile in CONF['genres'].items():
        assert len(profile['beats']) == 2, name
        assert all(0 < len(beat['text']) < 25 for beat in profile['beats'])
        assert profile['accent'].startswith('#')

def test_overlay_only_header():
    o = make_overlay(CONF['genres']['雑学・科学']['beats'][0], '#55ebc8', .5)
    assert o.shape == (H,W,4)
    assert o[260, 80, 3] > 0
    assert o[700, 450, 3] == 0
    assert o[1420, 450, 3] == 0
    assert o[1840, 500, 3] == 0

def test_timing():
    assert FIRST_SCENE_END == 70 and BREAK == 28
    assert 0 < BREAK / 30 < 1.5
    assert FIRST_SCENE_END / 30 < 3
