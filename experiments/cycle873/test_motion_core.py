import pytest
from quality_core import GENRES,validate_layout,validate_scenes
from motion_core import (validate_motion,base_motion_filter,focus_filters,FocusCue,FOCUS_CUES,
                         PAN_X_CENTER,PAN_X_AMPLITUDE,PAN_Y_CENTER,PAN_Y_AMPLITUDE,SCALED_W,SCALED_H)
def test_ten_genres():
    assert len(GENRES)==10
    for genre in GENRES:assert validate_motion(genre)
def test_safe_original_layout():assert validate_layout() and validate_scenes()
def test_overscan_safe():
    assert PAN_X_CENTER+PAN_X_AMPLITUDE<=SCALED_W-1080
    assert PAN_Y_CENTER+PAN_Y_AMPLITUDE<=SCALED_H-1920
def test_motion_filter_has_30fps_and_pan():
    f=base_motion_filter()
    assert 'fps=30' in f and 'sin(n/17)' in f and 'cos(n/21)' in f
def test_focus_is_inside_video_not_caption():
    for cue in FOCUS_CUES:assert cue.box[3]<1480
def test_reject_invalid_genre():
    with pytest.raises(ValueError):validate_motion('not-a-genre')
def test_reject_subtitle_collision():
    with pytest.raises(ValueError):validate_motion(cues=[FocusCue(1,2,(100,1450,400,1550),'bad')])
def test_reject_invalid_time():
    with pytest.raises(ValueError):validate_motion(cues=[FocusCue(5,4,(100,500,400,800),'bad')])
def test_focus_filter_has_time_window():
    f=focus_filters()
    assert 'drawbox' in f and '11.65' in f and '14.0' in f
