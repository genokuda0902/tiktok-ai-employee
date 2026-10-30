import importlib.util
from pathlib import Path
import pytest
p=Path(__file__).resolve().parents[1]/'source'/'scene_wipe.py'
s=importlib.util.spec_from_file_location('scene_wipe',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def test_ten_genres():
    assert len(m.GENRES)==10
    assert 'ai_work' in m.GENRES

def test_subtitle_protected():
    assert m.CROP_BOTTOM<m.SUBTITLE_TOP
    assert m.CROP_TOP>0

def test_transition_uses_last_old_frame():
    f=m.filtergraph(256)
    assert 'start_frame=255:end_frame=256' in f
    assert 'crop=1080:1110:0:140' in f
    assert 'eof_action=repeat' in f

def test_transition_frame_timing():
    f=m.filtergraph(256)
    assert '8.533333' in f and '8.900000' in f

def test_invalid_cuts():
    for args in ((1,100),(99,100),(256,266),(1.2,100),(30,50,16)):
        with pytest.raises(ValueError):m.validate_cut(*args)

def test_review_gate(tmp_path):
    with pytest.raises(ValueError,match='review'):
        m.render('missing.mp4',tmp_path/'o.mp4',tmp_path/'q.json','0'*64)

def test_unknown_genre(tmp_path):
    with pytest.raises(ValueError,match='unknown genre'):
        m.render('missing.mp4',tmp_path/'o.mp4',tmp_path/'q.json','0'*64,'unknown',True)

def test_other_genre_fails_closed(tmp_path):
    with pytest.raises(ValueError,match='approved source'):
        m.render('missing.mp4',tmp_path/'o.mp4',tmp_path/'q.json','0'*64,'beauty',True)

def test_no_existing_source(tmp_path):
    with pytest.raises(ValueError,match='missing source'):
        m.render('missing.mp4',tmp_path/'o.mp4',tmp_path/'q.json','0'*64,'ai_work',True)

def test_sha_rejects_tampering(tmp_path):
    source=tmp_path/'s.mp4';source.write_bytes(b'fake')
    with pytest.raises(ValueError,match='SHA256 mismatch'):
        m.render(source,tmp_path/'o.mp4',tmp_path/'q.json','0'*64,'ai_work',True)
