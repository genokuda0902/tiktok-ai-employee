"""Synthetic-only CI tests; private completed video is never uploaded."""
import numpy as np
import pytest
from scene_wipe import CUTS, GENRES, WIPE_FRAMES, wipe_alpha, wipe_art, validate


def test_cuts_are_seven_ordered_nonoverlapping():
    assert len(CUTS) == 7
    assert list(CUTS) == sorted(CUTS)
    assert all(b - a > WIPE_FRAMES for a, b in zip(CUTS, CUTS[1:]))


def test_ten_genres_and_review_gate(tmp_path):
    assert len(GENRES) == 10
    dummy = tmp_path / "not_approved.mp4"
    dummy.write_bytes(b"not an approved media source")
    for genre in GENRES:
        with pytest.raises(ValueError):
            validate(dummy, genre)


def test_unknown_genre_fails(tmp_path):
    dummy = tmp_path / "x.mp4"
    dummy.write_bytes(b"x")
    with pytest.raises(ValueError, match="unknown"):
        validate(dummy, "unknown")


@pytest.mark.parametrize("step", range(WIPE_FRAMES))
def test_wipe_alpha_range_and_monotonicity(step):
    a = wipe_alpha(step, width=100)
    assert a.shape == (1, 100, 1)
    assert a.min() >= 0 and a.max() <= 1
    if step:
        assert np.all(a >= wipe_alpha(step - 1, width=100) - 1e-6)


def test_last_wipe_frame_is_fully_new():
    assert np.all(wipe_alpha(WIPE_FRAMES - 1, width=300) == 1)


def test_subtitle_band_untouched():
    old = np.full((30, 100, 3), 20, dtype=np.uint8)
    new = np.full((30, 100, 3), 220, dtype=np.uint8)
    new[20:] = [30, 70, 180]
    for step in range(WIPE_FRAMES):
        out = wipe_art(old, new, step, art_end=20)
        assert np.array_equal(out[20:], new[20:])
        assert out.dtype == np.uint8


def test_first_wipe_frame_contains_both_scenes():
    old = np.zeros((20, 100, 3), dtype=np.uint8)
    new = np.full_like(old, 255)
    result = wipe_art(old, new, 0, art_end=10)
    assert 0 < result[:10].mean() < 255


@pytest.mark.parametrize("step", [-1, WIPE_FRAMES, 100])
def test_invalid_step_fails(step):
    with pytest.raises(ValueError):
        wipe_alpha(step)


def test_invalid_frame_shape_fails():
    with pytest.raises(ValueError):
        wipe_art(np.zeros((10, 10, 3)), np.zeros((11, 10, 3)), 0)
