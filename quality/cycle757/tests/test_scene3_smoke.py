from pathlib import Path
import json
import sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from scene3_editorial import scene_image,STAGES

def test_three_distinct_slides():
    images=[scene_image(i) for i in range(3)]
    assert all(im.size==(1080,1920) for im in images)
    assert len({im.tobytes() for im in images})==3

def test_cue_boundaries():
    assert STAGES[0][0]==4.0
    assert STAGES[1][1]==STAGES[2][0]==5.1
    assert STAGES[-1][1]==6.0

def test_genres_and_japanese_subtitles():
    assert len(json.loads((ROOT/'config/genres.json').read_text())['genres'])==10
    s=(ROOT/'config/phrase_cues.srt').read_text()
    assert s.count('-->')==16
    assert '画面につなげば、' in s and '操作できる。' in s

def test_tiktok_bottom_safe_zone():
    for i in range(3):
        im=scene_image(i).convert('L')
        assert im.crop((0,1680,1080,1920)).getextrema()[1] < 30
