import pytest
from video_engine.pattern_interrupt import PatternInterrupt, ffmpeg_values


def test_defaults_are_subtle_and_first_second():
    values = ffmpeg_values()
    assert 0 <= values["start"] < values["end"] <= 3.0
    assert values["zoom"] <= 1.05
    assert values["contrast"] <= 1.10


def test_rejects_late_interrupt():
    with pytest.raises(ValueError):
        ffmpeg_values(PatternInterrupt(start=3.1, end=3.3))


def test_rejects_aggressive_zoom():
    with pytest.raises(ValueError):
        ffmpeg_values(PatternInterrupt(zoom=1.10))
