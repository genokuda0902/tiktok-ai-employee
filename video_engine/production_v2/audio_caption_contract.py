"""Fail-closed audio/caption timing contract shared by all content genres."""
from __future__ import annotations

MIN_SCENE_SECONDS = 0.45
MAX_SCENE_SECONDS = 5.0
MIN_TOTAL_SECONDS = 15.0
MAX_TOTAL_SECONDS = 25.0

def build_caption_timeline(scenes, measured_durations):
    if not scenes or len(scenes) != len(measured_durations):
        raise ValueError("scene/duration mismatch")
    out=[]
    cursor=0.0
    for scene, raw_duration in zip(scenes, measured_durations):
        narration=str(scene.get("narration","")).strip()
        caption=str(scene.get("caption","")).strip()
        duration=float(raw_duration)
        if not narration or not caption:
            raise ValueError("narration and caption are required")
        if not MIN_SCENE_SECONDS <= duration <= MAX_SCENE_SECONDS:
            raise ValueError("measured scene duration out of range")
        start=round(cursor,3)
        cursor += duration
        out.append({
            "scene_id": scene.get("id") or scene.get("scene_id"),
            "start": start,
            "end": round(cursor,3),
            "caption": caption,
        })
    if not MIN_TOTAL_SECONDS <= cursor <= MAX_TOTAL_SECONDS:
        raise ValueError("measured total duration out of range")
    return out
