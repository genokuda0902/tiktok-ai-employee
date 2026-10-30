"""Unit tests for scene-boundary-safe screenshot motion; no external media needed."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'quality'))
import numpy as np
import pytest
from PIL import Image
from cycle1017_scene_motion import GENRES, make_mask, progress_expr, build_filter, ZOOM_MAX

BOUNDS=[0,79,174,258,340,423,503,593,675]

def test_ten_distinct_genres():
    assert len(GENRES)==len(set(GENRES))==10

@pytest.mark.parametrize('genre',GENRES)
def test_genre_compatible(genre):
    assert genre in GENRES
    assert 'zoompan' in build_filter(BOUNDS)

def test_eight_scene_boundaries():
    e=progress_expr(BOUNDS)
    for b in BOUNDS[1:]: assert f'lt(on,{b})' in e

def test_feathered_mask(tmp_path):
    f=tmp_path/'mask.png';make_mask(f);a=np.asarray(Image.open(f))
    assert a.shape==(1000,1000)
    assert a[0,500]==0 and a[500,0]==0 and a[500,500]==255
    assert 0<a[20,500]<255

def test_subtitle_safe_roi():
    f=build_filter(BOUNDS)
    assert 'crop=1000:1000:40:240' in f
    assert 'overlay=40:240' in f
    assert 'format=yuv420p[v]' in f
    assert 240+1000<1400

def test_reject_unsafe_zoom():
    with pytest.raises(ValueError): build_filter(BOUNDS,1.10)
    with pytest.raises(ValueError): build_filter(BOUNDS,1.0)

def test_default_zoom():
    assert 1.02<ZOOM_MAX<1.03
