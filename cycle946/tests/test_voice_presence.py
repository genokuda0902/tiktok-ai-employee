import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from voice_presence import GENRES,filter_chain,band_energy_ratio,speech_activity,boundary_audit,render

@pytest.mark.parametrize('genre',GENRES)
def test_genre_filter_is_safe_and_deterministic(genre):
    assert filter_chain(genre)==filter_chain('ai_work')
    assert 'highpass=' in filter_chain(genre)

def test_unknown_genre_fail_closed():
    with pytest.raises(ValueError):filter_chain('unsafe')

def test_band_ratio_synthetic():
    rate=16000;t=np.arange(rate)/rate
    a=np.sin(2*np.pi*200*t).astype(np.float32)
    b=a+.1*np.sin(2*np.pi*2400*t).astype(np.float32)
    assert band_energy_ratio(b)>band_energy_ratio(a)+10

def test_invalid_audio_fails():
    with pytest.raises(ValueError):band_energy_ratio(np.array([np.nan]*2000))

def test_boundary_audit_is_non_semantic():
    a=np.zeros(16000*23,dtype=np.float32)
    a[16000*2:16000*4]=.3
    report=boundary_audit(a)
    assert len(report)==7
    assert report[0]['human_timing_review']
    assert not report[-1]['human_timing_review']

def test_speech_activity_detects_non_speech_energy():
    a=np.zeros(16000,dtype=np.float32);a[8000:]=.15
    assert speech_activity(a)[-1]

def test_render_rejects_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError):render(tmp_path/'missing.mp4',tmp_path/'out.mp4')
