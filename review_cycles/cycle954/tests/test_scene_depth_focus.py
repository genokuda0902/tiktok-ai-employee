import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_depth_focus import (
    GENRE_PRESETS, APPROVED_GEOMETRY, SCENE_START, SCENE_END,
    WIDTH, HEIGHT, make_mask, temporal_strength, transform, validate_source,
)

@pytest.fixture(scope="module")
def mask():
    return make_mask("ai_work")

@pytest.fixture(scope="module")
def frame():
    im = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    # Synthetic paper, background checkerboard, and protected caption stripe.
    im[300:1200] = 100
    for y in range(320, 1160, 24):
        im[y:y+12, :100] = 250
    im[400:1040, 130:790] = 230
    im[1240:1470] = 42
    im[:300] = 80
    return im

def test_ten_genres_registered():
    assert len(GENRE_PRESETS) == 10

def test_fail_closed_unreviewed_genres():
    for genre in GENRE_PRESETS:
        if genre not in APPROVED_GEOMETRY:
            with pytest.raises(ValueError, match="unreviewed"):
                make_mask(genre)

def test_unknown_genre_rejected():
    with pytest.raises(ValueError):
        make_mask("unlisted")

def test_bad_dimensions_rejected():
    with pytest.raises(ValueError):
        make_mask("ai_work", 720, 1280)

def test_temporal_window():
    assert temporal_strength(5.7) == 0
    assert temporal_strength(6.5) == 1
    assert temporal_strength(8.71) == 0
    assert 0 < temporal_strength(5.9) < 1

def test_mask_paper_protected(mask):
    assert mask[690, 440] < 0.001
    assert mask[700, 40] > 0.95

def test_mask_caption_header_protected(mask):
    assert np.max(mask[:300]) == 0
    assert np.max(mask[1200:]) == 0

def test_transform_off_time_bit_exact(frame, mask):
    assert np.array_equal(transform(frame, 5.0, "ai_work", mask), frame)

def test_transform_protected_regions_bit_exact(frame, mask):
    out = transform(frame, 6.5, "ai_work", mask)
    assert np.array_equal(out[:300], frame[:300])
    assert np.array_equal(out[1240:], frame[1240:])
    assert np.array_equal(out[600:700, 250:700], frame[600:700, 250:700])

def test_transform_changes_background(frame, mask):
    out = transform(frame, 6.5, "ai_work", mask)
    assert np.mean(np.abs(out[400:900, :70].astype(int) - frame[400:900, :70])) > 4

def test_transform_preserves_dimensions(frame, mask):
    assert transform(frame, 6.5, "ai_work", mask).shape == frame.shape

def test_hash_lock(tmp_path):
    source = tmp_path / "source.mp4"
    source.write_bytes(b"not approved")
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_source(source, "ai_work")

def test_no_unapproved_genre_media(tmp_path):
    source = tmp_path / "source.mp4"
    source.write_bytes(b"not approved")
    with pytest.raises(ValueError, match="unreviewed"):
        validate_source(source, "travel")
