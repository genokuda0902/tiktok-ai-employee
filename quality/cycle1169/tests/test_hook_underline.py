import sys
from pathlib import Path
import pytest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from hook_underline import ROI, COLORS, INTRO_FRAMES, opacity_and_progress, draw_frame, validate, overlays

def test_palette_has_ten_genres():
    assert len(COLORS)==10
    assert validate()
@pytest.mark.parametrize('genre',list(COLORS))
def test_genre_generates_rgba(genre):
    im=draw_frame(17,genre)
    assert im.size==ROI[2:]
    assert im.mode=='RGBA'
    assert np.asarray(im)[:,:,3].max()>0
@pytest.mark.parametrize('frame',[0,1,2,3,41])
def test_blank_at_start_and_end(frame):
    assert np.asarray(draw_frame(frame))[:,:,3].max()==0

def test_line_draws_monotonically():
    ps=[opacity_and_progress(n)[0] for n in range(4,22)]
    assert all(a<=b for a,b in zip(ps,ps[1:]))
    assert ps[-1]==1

def test_fade_drops_monotonically():
    a=[opacity_and_progress(n)[1] for n in range(29,42)]
    assert all(x>=y for x,y in zip(a,a[1:]))

def test_no_subtitle_overlap():
    x,y,w,h=ROI
    assert y+h<410 and y+h<1150

def test_reject_bad_roi():
    with pytest.raises(ValueError): validate(roi=(75,1250,540,18))

def test_reject_invalid_genre():
    with pytest.raises(ValueError): draw_frame(10,'unknown')

def test_reject_out_of_range_frames():
    with pytest.raises(ValueError): opacity_and_progress(-1)
    with pytest.raises(ValueError): opacity_and_progress(INTRO_FRAMES)

def test_overlay_count(tmp_path):
    assert overlays(tmp_path)==INTRO_FRAMES
    assert len(list(tmp_path.glob('hook_*.png')))==INTRO_FRAMES
