"""Regression tests for canonical scene identity in synthesized captions."""
import pytest
from video_engine.production_v2 import aivis_narration as a

def scene(sid="s1"):
    return {"scene_id": sid, "caption": "字幕", "narration": "声"}

def test_scene_id_preserved():
    out = a._caption_timeline([(scene(), b"", 2.0, "声", "字幕")])
    assert out == [{"scene_id": "s1", "start": 0.0, "end": 2.0, "text": "字幕"}]

def test_legacy_scene_id_supported():
    assert a._scene_id({"id": "old"}) == "old"

def test_conflicting_ids_rejected():
    with pytest.raises(RuntimeError, match="Conflicting"):
        a._scene_id({"id": "old", "scene_id": "new"})

def test_missing_id_rejected():
    with pytest.raises(RuntimeError, match="Missing"):
        a._scene_id({"caption": "字幕"})

def test_duplicate_scene_id_rejected():
    with pytest.raises(RuntimeError, match="Duplicate"):
        a._scene_lines({"scenes": [scene(), scene()]})

def test_positive_measured_duration_required():
    with pytest.raises(RuntimeError, match="positive"):
        a._caption_timeline([(scene(), b"", 0.0, "声", "字幕")])
