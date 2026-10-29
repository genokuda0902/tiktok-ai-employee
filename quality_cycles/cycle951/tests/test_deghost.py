import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pytest
from deghost_transition import GENRE_BACKGROUNDS,SCENE_CUTS,window,fade_alpha,make_feather_mask

@pytest.mark.parametrize('genre',list(GENRE_BACKGROUNDS))
def test_genre_has_valid_dark_palette(genre):
    rgb=GENRE_BACKGROUNDS[genre]
    assert len(rgb)==3 and all(0<=v<=45 for v in rgb)

@pytest.mark.parametrize('cut',SCENE_CUTS)
def test_windows_in_bounds(cut):
    s,e=window(cut)
    assert 0<s<e<691 and e-s==11

@pytest.mark.parametrize('cut',SCENE_CUTS)
def test_no_double_exposure_single_snapshot(cut):
    s,e=window(cut)
    assert all(0.10 <= fade_alpha(i,s,e) <= 1.0 for i in range(s,e))
    assert fade_alpha(s,s,e)>fade_alpha((s+e)//2,s,e)
    assert fade_alpha(e-1,s,e)>fade_alpha((s+e)//2,s,e)

def test_protect_header_and_caption():
    mask=make_feather_mask(1920,1080)
    assert mask.shape==(1920,1,1)
    assert mask[50,0,0]==0 and mask[1700,0,0]==0
    assert mask[600,0,0]==1
    assert 0<mask[160,0,0]<1

def test_bad_window_raises():
    s,e=window(2.8)
    with pytest.raises(ValueError): fade_alpha(s-1,s,e)
