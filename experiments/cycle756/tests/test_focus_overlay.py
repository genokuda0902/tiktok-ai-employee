import sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from focus_overlay import W,H,MARKERS,STAGES,overlay,generate_assets

def test_resolution_and_transparency():
    a=overlay(0)
    assert a.size==(1080,1920)
    assert a.getpixel((1000,1800))[3]==0

def test_safe_area():
    for m in MARKERS:
        x,y=m['center']
        assert 60<x<760 and 830<y<920
    for stage in [-1,0,1,2]:
        a=overlay(stage).getchannel('A')
        assert a.crop((800,0,W,H)).getbbox() is None
        assert a.crop((0,1200,W,H)).getbbox() is None

def test_timeline():
    assert STAGES[0][0]==6.0 and STAGES[-1][1]==8.0
    assert [s[2] for s in STAGES]==[-1,0,1,2]
    assert all(a[1]<=b[0] for a,b in zip(STAGES,STAGES[1:]))

def test_stage_visual_difference():
    assert overlay(0).tobytes()!=overlay(1).tobytes()

def test_assets(tmp_path):
    assert len(generate_assets(tmp_path))==4
    assert all(Image.open(p).mode=='RGBA' for p in tmp_path.iterdir())
