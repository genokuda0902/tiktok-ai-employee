"""Genre-independent caption timing helpers.

Pure-Python and deterministic: timing is derived only from measured narration
durations. This module does not synthesize speech, publish media, or approve
content.
"""
from __future__ import annotations


def build_caption_timeline(scenes, durations):
    """Return caption start/end times from measured per-scene durations.

    Fails closed on missing captions, count mismatch, non-positive durations,
    or segments outside the 0.45-5.0 second narration quality window.
    """
    if not scenes:
        raise ValueError("scenes required")
    if len(scenes) != len(durations):
        raise ValueError("scene/duration count mismatch")

    timeline = []
    cursor = 0.0
    for scene, seconds in zip(scenes, durations):
        caption = str(scene.get("caption") or scene.get("message") or "").strip()
        if not caption:
            raise ValueError(f"scene {scene.get('id')} missing caption")
        seconds = float(seconds)
        if not 0.45 <= seconds <= 5.0:
            raise ValueError(f"scene {scene.get('id')} duration outside 0.45-5.0s")
        start = cursor
        end = start + seconds
        timeline.append({
            "scene_id": scene.get("id"),
            "start": round(start, 3),
            "end": round(end, 3),
            "text": caption,
        })
        cursor = end

    if not 15.0 <= cursor <= 25.0:
        raise ValueError(f"total measured narration outside 15-25s: {cursor:.3f}s")
    return timeline
