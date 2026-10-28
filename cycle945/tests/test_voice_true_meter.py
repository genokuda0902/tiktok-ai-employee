import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from voice_true_meter import (GENRES, PALETTES, frame_levels, level_to_height, meter_image,
                              OVERLAY_Y, OVERLAY_H, TEXT_SAFE_END_Y, PROGRESS_SAFE_START_Y)

@pytest.mark.parametrize('genre',GENRES)
def test_ten_genres_are_deterministic_and_safe(genre):
    levels=np.array([.001,.08,.3,.02]*20,dtype=np.float32)
    a=meter_image(levels,40,genre)
    b=meter_image(levels,40,genre)
    assert a.size==(440,66) and a.mode=='RGBA'
    assert a.tobytes()==b.tobytes()
    assert PALETTES[genre]

def test_real_energy_drives_meter_not_random():
    sr=16000
    a=np.zeros(sr*2,dtype=np.float32)
    a[sr:]=.2*np.sin(2*np.pi*220*np.arange(sr)/sr)
    levels=frame_levels(a,60)
    assert np.max(levels[:29])==0
    assert np.mean(levels[35:]) > .1
    assert level_to_height(float(levels[45]))>level_to_height(float(levels[10]))+20

def test_fail_closed_on_invalid_inputs():
    with pytest.raises(ValueError): meter_image(np.ones(40),20,'other')
    with pytest.raises(ValueError): frame_levels(np.array([float('nan')]),30)
    with pytest.raises(ValueError): frame_levels(np.ones((3,2)),30)
    with pytest.raises(IndexError): meter_image(np.ones(5),5)
    with pytest.raises(ValueError): level_to_height(-1)

def test_caption_text_and_progress_are_outside_overlay():
    assert OVERLAY_Y>TEXT_SAFE_END_Y
    assert OVERLAY_Y+OVERLAY_H<PROGRESS_SAFE_START_Y

def test_silence_is_safe_and_nonzero_display():
    assert level_to_height(0)==3
    assert level_to_height(1)>level_to_height(.2)
