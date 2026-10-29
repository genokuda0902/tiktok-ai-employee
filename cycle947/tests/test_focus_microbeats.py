import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from focus_microbeats import GENRE_PROFILES,SCENE_BOUNDARIES,SCENE_TARGETS,beat_scale,focus_content,scene_index,smoothstep

def test_ten_genres_safe():
    assert len(GENRE_PROFILES)==10
    assert all(1.0<v<=1.10 for v in GENRE_PROFILES.values())

def test_eight_scenes():
    assert len(SCENE_BOUNDARIES)==9 and len(SCENE_TARGETS)==8
    assert all(b>a for a,b in zip(SCENE_BOUNDARIES,SCENE_BOUNDARIES[1:]))

def test_first_half_unmodified():
    for s in range(8):
        a,b=SCENE_BOUNDARIES[s:s+2]
        assert beat_scale(a+0.20*(b-a),a,b,1.055)==1.0

def test_second_half_zooms():
    for s in range(8):
        a,b=SCENE_BOUNDARIES[s:s+2]
        assert beat_scale(a+0.9*(b-a),a,b,1.055)>1.05

def test_scale_monotonic():
    v=[beat_scale(x/100,0,1,1.06) for x in range(100)]
    assert all(a<=b for a,b in zip(v,v[1:]))

def test_preserves_protected_regions_exact():
    rng=np.random.default_rng(42)
    src=rng.integers(0,255,(120,80,3),dtype=np.uint8)
    out=focus_content(src,1.06,rect=(10,20,70,80))
    assert np.array_equal(src[:20],out[:20]); assert np.array_equal(src[80:],out[80:])
    assert np.array_equal(src[:,:10],out[:,:10]); assert np.array_equal(src[:,70:],out[:,70:])
    assert np.any(src[20:80,10:70]!=out[20:80,10:70])

def test_noop():
    src=np.zeros((120,80,3),dtype=np.uint8)
    assert np.array_equal(src,focus_content(src,1.0,rect=(10,20,70,80)))

def test_reject_unsafe_scale():
    with pytest.raises(ValueError):focus_content(np.zeros((120,80,3),dtype=np.uint8),1.2,rect=(10,20,70,80))

def test_reject_bad_target():
    with pytest.raises(ValueError):focus_content(np.zeros((120,80,3),dtype=np.uint8),1.04,target=(2,0),rect=(10,20,70,80))

def test_scene_indices():
    assert scene_index(0)==0 and scene_index(2.9)==1 and scene_index(22.9)==7

def test_smoothstep_bounded():
    assert smoothstep(-1)==0 and smoothstep(2)==1 and smoothstep(.5)==.5
