import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pytest
from accent_bloom import bloom_frame, validate, GENRE_HUES


def test_ten_genre_profiles():
    assert len(GENRE_HUES)==10
    for name in GENRE_HUES: validate(1080,1920,30,name,150,1180,28,synthetic=True)


def test_unreviewed_real_layout_rejected():
    with pytest.raises(ValueError): validate(1080,1920,30,'money',150,1180,28)


def test_protected_caption_identical_before_compression():
    f=np.zeros((1920,1080,3),np.uint8)
    f[400:500,100:900]=(180,200,0)
    f[1250:1550]=(20,20,20)
    out=bloom_frame(f)
    assert np.array_equal(f[1180:],out[1180:])
    assert np.array_equal(f[:150],out[:150])


def test_cyan_halo_visible_but_bounded():
    f=np.zeros((1920,1080,3),np.uint8)
    f[500:540,500:540]=(220,220,0)
    out=bloom_frame(f)
    assert out[520,520,1]>=f[520,520,1]
    assert out[496,520,1]>f[496,520,1]
    assert np.max(out.astype(np.int16)-f.astype(np.int16))<=30


def test_neutral_white_untouched():
    f=np.full((1920,1080,3),180,np.uint8)
    assert np.array_equal(f,bloom_frame(f))


def test_reject_bad_strength():
    with pytest.raises(ValueError): bloom_frame(np.zeros((1920,1080,3),np.uint8),strength=31)


def test_reject_wrong_frame_type():
    with pytest.raises(ValueError): bloom_frame(np.zeros((1920,1080),np.uint8))
