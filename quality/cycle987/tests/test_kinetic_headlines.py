import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import numpy as np
import pytest
from kinetic_headlines import (GENRES,TITLES,SCENE_BOUNDARIES,make_card,
    render_frame,scene_for_frame,ease_out_cubic,WIDTH,HEIGHT,LAYOUT)

@pytest.fixture(scope='module')
def cards():
    return [make_card(GENRES['ai_work'],s) for s in TITLES]

@pytest.mark.parametrize('i',range(8))
def test_scene_boundaries(i):
    s,offset=scene_for_frame(SCENE_BOUNDARIES[i]);assert s==i and offset==0

@pytest.mark.parametrize('genre',list(GENRES))
def test_all_genre_palette_can_render(genre):
    card,label,fs=make_card(GENRES[genre],TITLES[0])
    assert card.shape==(LAYOUT.h,LAYOUT.w,4)
    assert label.shape==card.shape
    assert 36<=fs<=50

def test_reveal_progress(cards):
    original=np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)
    a=render_frame(original.copy(),0,cards)
    b=render_frame(original.copy(),14,cards)
    region=lambda x:x[LAYOUT.y:LAYOUT.y+LAYOUT.h,LAYOUT.x:LAYOUT.x+LAYOUT.w]
    assert np.count_nonzero(region(b)!=region(a))>3000

def test_caption_and_footer_pixels_preserved_before_codec(cards):
    src=np.random.default_rng(123).integers(0,256,(HEIGHT,WIDTH,3),dtype=np.uint8)
    out=render_frame(src.copy(),87,cards)
    assert np.array_equal(out[1180:,:,:],src[1180:,:,:])
    assert np.array_equal(out[:188,:,:],src[:188,:,:])

def test_scene_changes_are_distinct(cards):
    src=np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)
    a=render_frame(src.copy(),25,cards)
    b=render_frame(src.copy(),112,cards)
    assert np.mean(np.abs(a.astype('int16')-b.astype('int16')))>0.01

def test_bad_frame_rejected(cards):
    with pytest.raises(ValueError):
        render_frame(np.zeros((1920,720,3),dtype=np.uint8),0,cards)

def test_easing_monotonic():
    values=[ease_out_cubic(i/20) for i in range(21)]
    assert values[0]==0 and values[-1]==1 and values==sorted(values)
