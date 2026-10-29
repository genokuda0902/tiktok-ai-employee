import importlib.util
from pathlib import Path
import pytest
p=Path(__file__).resolve().parents[1]/'src'/'action_focus.py'
s=importlib.util.spec_from_file_location('action_focus',p); m=importlib.util.module_from_spec(s)
import sys
sys.modules[s.name]=m;s.loader.exec_module(m)
HASH='0'*64

def test_ten_genres():
    for genre in m.GENRES:
        m.FocusSpec(genre,HASH,(m.Beat(1,2,(100,100,200,200),'action'),)).validate()

def test_reviewed_spec_valid():
    spec=m.reviewed_ai_work_spec(HASH);spec.validate();assert len(spec.beats)==2

def test_caption_region_protected():
    with pytest.raises(ValueError):m.Beat(1,2,(100,1430,200,100),'bad').validate()

def test_negative_rect_rejected():
    with pytest.raises(ValueError):m.Beat(1,2,(-1,10,100,100),'bad').validate()

def test_out_of_frame_rejected():
    with pytest.raises(ValueError):m.Beat(1,2,(1000,10,200,100),'bad').validate()

def test_overlap_rejected():
    with pytest.raises(ValueError):m.FocusSpec('ai_work',HASH,(m.Beat(1,2,(1,1,100,100),'a'),m.Beat(1.9,3,(1,1,100,100),'b'))).validate()

def test_unordered_rejected():
    with pytest.raises(ValueError):m.FocusSpec('ai_work',HASH,(m.Beat(3,4,(1,1,100,100),'a'),m.Beat(1,2,(1,1,100,100),'b'))).validate()

def test_unknown_genre_rejected():
    with pytest.raises(ValueError):m.FocusSpec('unknown',HASH,(m.Beat(1,2,(1,1,100,100),'a'),)).validate()

def test_bad_hash_rejected():
    with pytest.raises(ValueError):m.FocusSpec('ai_work','bad',(m.Beat(1,2,(1,1,100,100),'a'),)).validate()

def test_missing_beats_rejected():
    with pytest.raises(ValueError):m.FocusSpec('ai_work',HASH,()).validate()

def test_too_short_rejected():
    with pytest.raises(ValueError):m.Beat(1,1.1,(1,1,100,100),'a').validate()

def test_too_long_rejected():
    with pytest.raises(ValueError):m.Beat(1,6,(1,1,100,100),'a').validate()

def test_filter_has_two_focus_beats():
    vf=m.video_filter(m.reviewed_ai_work_spec(HASH));assert vf.count('drawbox=')==4;assert 'between(t,13.000,14.360)' in vf

def test_no_caption_overlay():
    for b in m.reviewed_ai_work_spec(HASH).beats:
        assert b.rect[1]+b.rect[3]<m.CONTENT_BOTTOM

def test_source_hash_fail_closed(tmp_path):
    f=tmp_path/'dummy.mp4';f.write_bytes(b'not a video')
    with pytest.raises(ValueError,match='SHA mismatch'):
        m.validate_source(f,m.reviewed_ai_work_spec(HASH))
