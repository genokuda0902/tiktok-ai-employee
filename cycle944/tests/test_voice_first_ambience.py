import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from voice_first_ambience import GENRES,generate_bed,duck_envelope,mix,SAMPLE_RATE

@pytest.mark.parametrize('genre',GENRES)
def test_ten_genres_deterministic_and_stereo(genre):
    a=generate_bed(2400,genre)
    b=generate_bed(2400,genre)
    assert a.shape==(2400,2) and np.array_equal(a,b)
    assert np.isfinite(a).all()

def test_ducking_reduces_under_speech():
    v=np.zeros((SAMPLE_RATE*2,2),dtype=np.float32)
    v[24000:72000]=.12
    env,active=duck_envelope(v)
    assert active.any()
    assert env[48000]<env[4000]*.5

def test_preserves_narration_and_peak():
    t=np.arange(SAMPLE_RATE,dtype=np.float32)/SAMPLE_RATE
    v=np.column_stack([.2*np.sin(2*np.pi*180*t)]*2).astype(np.float32)
    out,qa=mix(v)
    assert out.shape==v.shape
    assert np.max(np.abs(out))<.95
    assert np.sqrt(np.mean((out-v)**2))<.01
    assert qa['genre']=='ai_work'

def test_fail_closed_genre():
    with pytest.raises(ValueError): generate_bed(100,'invalid')
