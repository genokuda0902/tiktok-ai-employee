"""Pure caption timeline helper for measured narration durations.

Reimplementation: original v33 source remains unavailable.
No publishing or external upload is performed here.
"""
from __future__ import annotations
from typing import Iterable, List, Dict, Any

def build_caption_timeline(scenes: Iterable[Dict[str, Any]], durations: Iterable[float], *, min_scene_seconds: float = 0.45, max_scene_seconds: float = 5.0, max_total_seconds: float = 25.0) -> List[Dict[str, Any]]:
    """Build a fail-closed caption timeline from measured audio durations."""
    scene_list = list(scenes)
    duration_list = [float(x) for x in durations]
    if not scene_list or len(scene_list) != len(duration_list):
        raise ValueError("scene/duration count mismatch")
    if any(d < min_scene_seconds or d > max_scene_seconds for d in duration_list):
        raise ValueError("measured narration duration outside quality bounds")
    if sum(duration_list) > max_total_seconds:
        raise ValueError("total narration duration exceeds quality bound")
    cursor = 0.0
    timeline: List[Dict[str, Any]] = []
    for index, (scene, duration) in enumerate(zip(scene_list, duration_list)):
        caption = str(scene.get("caption") or scene.get("narration") or "").strip()
        if not caption:
            raise ValueError(f"scene {index} has no caption/narration")
        start = round(cursor, 3)
        end = round(cursor + duration, 3)
        timeline.append({"scene_index": index, "start": start, "end": end, "text": caption})
        cursor += duration
    return timeline
