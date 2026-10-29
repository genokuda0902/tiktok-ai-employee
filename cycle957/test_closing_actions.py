import tempfile
from pathlib import Path
import numpy as np
import pytest
from closing_actions import GENRES, WIDTH, TOP_END, START_FRAME, END_FRAME, stage_at, render_upper, validate

def test_ten_genre_configurations():
    assert len(GENRES)==10
    assert all(len(x)==3 for x in GENRES.values())

@pytest.mark.parametrize('genre',list(GENRES)[1:])
def test_unreviewed_genres_fail_closed(genre):
    with pytest.raises(ValueError,match='not reviewed'):render_upper(620,genre)

def test_stage_boundaries():
    assert stage_at(START_FRAME-1)==-1
    assert stage_at(START_FRAME)==0
    assert stage_at(638)==1
    assert stage_at(665)==2
    assert stage_at(END_FRAME)==-1

@pytest.mark.parametrize('frame',[610,639,680])
def test_render_geometry(frame):
    im=render_upper(frame)
    assert im.shape==(TOP_END,WIDTH,3)
    assert im.dtype==np.uint8
    assert im.mean()>15

def test_three_distinct_visual_stages():
    a,b,c=[render_upper(x).astype('int16') for x in (610,639,680)]
    assert np.abs(a-b).mean()>1
    assert np.abs(b-c).mean()>1

def test_invalid_time_fails():
    with pytest.raises(ValueError):render_upper(START_FRAME-1)

def test_source_and_approval_gates():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'fake.mp4';p.write_bytes(b'wrong')
        with pytest.raises(ValueError,match='SHA'):validate('ai_work',p)
        with pytest.raises(ValueError,match='review only'):validate('ai_work',p,review_only=False)
        with pytest.raises(ValueError,match='review only'):validate('ai_work',p,publication_approved=True)
        with pytest.raises(ValueError,match='unknown genre'):validate('invalid',p)
