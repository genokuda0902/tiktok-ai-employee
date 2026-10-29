import hashlib
from pathlib import Path
import sys
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from midtone_lift import GENRE_GAMMA, mask_array, WIDTH, HEIGHT, render

@pytest.mark.parametrize('genre,gamma', list(GENRE_GAMMA.items()))
def test_ten_genre_presets_are_safe(genre, gamma):
    assert genre and 1.0 < gamma <= 1.16

def test_mask_preserves_subtitle_and_header():
    m=mask_array()
    assert m.shape==(HEIGHT,WIDTH)
    assert np.count_nonzero(m[:405])==0
    assert np.count_nonzero(m[1410:])==0
    assert m[900,540]==255
    assert m[420,540]==0
    assert m[1289,540]==0

def test_mask_feather():
    m=mask_array()
    assert 0 < m[450,540] < 255
    assert m[550,540]==255
    assert 0 < m[900,70] < 255

def test_mask_invalid_bounds():
    with pytest.raises(ValueError): mask_array(bounds=(0,0,1100,100))
    with pytest.raises(ValueError): mask_array(feather=0)

def test_unreviewed_genre_fails_closed(tmp_path):
    src=tmp_path/'source.mp4'; src.write_bytes(b'synthetic')
    digest=hashlib.sha256(b'synthetic').hexdigest()
    with pytest.raises(PermissionError):
        render(src,tmp_path/'out.mp4','finance',expected_sha=digest)
    assert not (tmp_path/'out.mp4').exists()

def test_unreviewed_source_fails_closed(tmp_path):
    src=tmp_path/'source.mp4'; src.write_bytes(b'synthetic')
    with pytest.raises(PermissionError): render(src,tmp_path/'out.mp4')
    assert not (tmp_path/'out.mp4').exists()

def test_unknown_genre_fails(tmp_path):
    src=tmp_path/'source.mp4'; src.write_bytes(b'synthetic')
    with pytest.raises(ValueError): render(src,tmp_path/'out.mp4','not_a_genre')
