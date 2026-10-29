import hashlib, tempfile
from pathlib import Path
import numpy as np
import pytest
from template_scene import GENRES, START, END, TOP_END, WIDTH, stage_at, render_upper, validate

def test_ten_genre_configurations():
    assert len(GENRES)==10
    assert all(len(v)==3 for v in GENRES.values())

@pytest.mark.parametrize('genre',list(GENRES)[1:])
def test_unreviewed_genre_fails_closed(genre):
    with pytest.raises(ValueError): render_upper(18.0,genre)

def test_stages():
    assert stage_at(START-0.01)==-1
    assert stage_at(17.50)==0
    assert stage_at(18.45)==1
    assert stage_at(19.60)==2
    assert stage_at(END)==-1

@pytest.mark.parametrize('t',[17.5,18.5,19.5])
def test_frame_geometry_and_visible_content(t):
    f=render_upper(t)
    assert f.shape==(TOP_END,WIDTH,3)
    assert f.dtype==np.uint8
    assert f.mean()>20


def test_stages_have_different_pixels():
    a,b,c=(render_upper(t) for t in [17.6,18.6,19.6])
    assert np.abs(a.astype('int16')-b.astype('int16')).mean()>1
    assert np.abs(b.astype('int16')-c.astype('int16')).mean()>1


def test_sha_and_publication_gate():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'x.mp4';p.write_bytes(b'not source')
        with pytest.raises(ValueError,match='SHA'):validate('ai_work',p)
        with pytest.raises(ValueError,match='review only'):validate('ai_work',p,review_only=False)
        with pytest.raises(ValueError,match='review only'):validate('ai_work',p,publication_approved=True)
        with pytest.raises(ValueError,match='unknown genre'):validate('missing',p)
