"""Fast offline tests; no reference media or credentials required."""
import json,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from render import validate_config,feather_mask,eased_focus,apply_focus
CFG=json.loads((ROOT/"motion.json").read_text(encoding="utf-8"))
def test_config():validate_config(CFG)
def test_ten_genres_reusable():
    assert len(CFG["shots"])==3
    assert CFG["canvas"]["width"]==1080 and CFG["canvas"]["height"]==1920
def test_light_eases():
    for s in CFG["shots"]:
        assert eased_focus(s["start_frame"],s)[0]==0
        assert abs(eased_focus(s["end_frame"]-1,s)[0])<1e-9
        assert eased_focus((s["start_frame"]+s["end_frame"])//2,s)[0]>.99
def test_mask():
    m=feather_mask(200,200,20)
    assert m.shape==(200,200) and m[0,0]==0 and m[100,100]==1
def test_static_untouched():
    a=np.zeros((1920,1080,3),dtype=np.uint8)
    assert apply_focus(a,20,CFG) is a
def test_caption_untouched():
    a=np.full((1920,1080,3),25,dtype=np.uint8)
    b=apply_focus(a,150,CFG)
    assert np.array_equal(a[1400:],b[1400:])
    assert np.array_equal(a[:300],b[:300])
    assert np.count_nonzero(a[500:1000,150:900]!=b[500:1000,150:900])>100
def test_reject_glow():
    c=json.loads(json.dumps(CFG));c["shots"][0]["max_glow"]=100
    with pytest.raises(AssertionError):validate_config(c)
def test_reject_subtitle_overlap():
    c=json.loads(json.dumps(CFG));c["roi"]["y"]=1100
    with pytest.raises(AssertionError):validate_config(c)
def test_reject_shot_overlap():
    c=json.loads(json.dumps(CFG));c["shots"][1]["start_frame"]=150
    with pytest.raises(AssertionError):validate_config(c)
