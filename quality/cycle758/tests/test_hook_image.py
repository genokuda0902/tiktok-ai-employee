import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from hook_reveal import scene_image,STAGES
def test_resolution():
    assert scene_image(1).size==(1080,1920)
def test_cue_boundaries():
    assert STAGES[1][0]==0.167 and STAGES[2][0]==1.0
def test_distinct_reveal():
    a=scene_image(1);b=scene_image(2)
    assert a.getpixel((120,405))!=b.getpixel((120,405))
