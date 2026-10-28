import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
import pytest
from adaptive_scene_wipe import GENRES, wipe

@pytest.mark.parametrize("genre",list(GENRES))
def test_genre_profile(genre):
    frames,feather=GENRES[genre]
    assert 5<=frames<=10 and 80<=feather<=200

def test_frame_contract():
    old=np.zeros((200,80,3),dtype=np.uint8)
    new=np.full_like(old,255)
    out=wipe(old,new,3,7,30)
    assert out.shape==old.shape and out.dtype==np.uint8

def test_progressive_reveal():
    old=np.zeros((200,80,3),dtype=np.uint8)
    new=np.full_like(old,255)
    scores=[wipe(old,new,i,7,30,protect_chrome=False).mean() for i in range(7)]
    assert all(a<b for a,b in zip(scores,scores[1:]))

def test_reverse_direction():
    old=np.zeros((200,80,3),dtype=np.uint8)
    new=np.full_like(old,255)
    out=wipe(old,new,2,7,30,direction=-1,protect_chrome=False)
    assert out[0,-1,0]>out[0,0,0]

def test_subtitle_header_footer_protected():
    old=np.zeros((200,80,3),dtype=np.uint8)
    new=np.full_like(old,255)
    out=wipe(old,new,0,7,30,protect_chrome=True)
    assert np.all(out[0]==255) and np.all(out[-1]==255)
    assert out[90].mean()<100

def test_invalid_beat():
    old=np.zeros((200,80,3),dtype=np.uint8)
    with pytest.raises(ValueError): wipe(old,old,7,7,30)

def test_invalid_feather():
    old=np.zeros((200,80,3),dtype=np.uint8)
    with pytest.raises(ValueError): wipe(old,old,1,7,0)
