import pytest

from video_engine.production_v2.pipeline import validate_measured_caption_timeline


def _scenes():
    return [
        {"scene_id": "s1", "duration": 1.0, "caption": "最初の一秒で変える"},
        {"scene_id": "s2", "duration": 1.2, "caption": "実測音声で字幕を合わせる"},
    ]


def _timeline():
    return [
        {"scene_id": "s1", "text": "最初の一秒で変える", "start": 0.0, "end": 1.0},
        {"scene_id": "s2", "text": "実測音声で字幕を合わせる", "start": 1.0, "end": 2.2},
    ]


def test_accepts_contiguous_measured_timeline():
    out = validate_measured_caption_timeline(
        _scenes(), _timeline(), "measured_aivis_scene_duration"
    )
    assert out[-1]["end"] == pytest.approx(2.2)


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda t: t.__setitem__(0, {**t[0], "text": "別字幕"}), "text mismatch"),
        (lambda t: t.__setitem__(1, {**t[1], "start": 1.1}), "gap/overlap"),
        (lambda t: t.__setitem__(1, {**t[1], "end": 2.0}), "duration mismatch"),
        (lambda t: t.__setitem__(1, {**t[1], "scene_id": "wrong"}), "scene ID mismatch"),
    ],
)
def test_rejects_drift(mutate, message):
    timeline = _timeline()
    mutate(timeline)
    with pytest.raises(ValueError, match=message):
        validate_measured_caption_timeline(
            _scenes(), timeline, "measured_aivis_scene_duration"
        )


def test_rejects_untrusted_source():
    with pytest.raises(ValueError, match="Untrusted measured caption timing source"):
        validate_measured_caption_timeline(_scenes(), _timeline(), "planned")
