import pytest
from video_engine.mobile_legibility_scale import LegibilityScale, ffmpeg_filter, posting_policy


def test_default_is_subtle_and_portrait_safe():
    f = ffmpeg_filter()
    assert "1.0180" in f
    assert "crop=1080:1920" in f


def test_rejects_overzoom():
    with pytest.raises(ValueError):
        ffmpeg_filter(LegibilityScale(scale=1.031))


def test_release_policy_remains_human_only():
    p = posting_policy()
    assert p["zero_cost"] is True
    assert p["human_approval_required"] is True
    assert p["auto_post"] is False
