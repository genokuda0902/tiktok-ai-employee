import pytest
from video_engine.semantic_sync_contract import Scene, validate_scene, validate_story


def scene(i=0):
    return Scene(f"image {i}", f"narration {i}", f"字幕{i}", 2.0)


def test_valid_story():
    validate_story([scene(i) for i in range(10)])


def test_rejects_too_few_scenes():
    with pytest.raises(ValueError):
        validate_story([scene(i) for i in range(7)])


def test_rejects_long_caption():
    with pytest.raises(ValueError):
        validate_scene(Scene("image", "narration", "長" * 29, 2.0))


def test_rejects_bad_duration():
    with pytest.raises(ValueError):
        validate_scene(Scene("image", "narration", "字幕", 0.5))
