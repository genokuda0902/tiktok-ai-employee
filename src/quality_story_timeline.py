"""Reusable 3-stage story timeline validation for 10 TikTok genres.

Review-only: no posting, no asset upload, no paid service.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    label: str

def validate_timeline(scenes, duration):
    if not scenes or duration <= 0:
        raise ValueError("timeline must not be empty")
    cursor = 0.0
    for scene in scenes:
        if abs(scene.start - cursor) > 1e-6 or scene.end <= scene.start:
            raise ValueError("timeline has gap, overlap or invalid duration")
        cursor = scene.end
    if abs(cursor - duration) > 1e-6:
        raise ValueError("timeline does not cover full video")
    return True

def scene_index_at(t, scenes):
    if t < 0 or t >= scenes[-1].end:
        raise ValueError("timestamp outside video")
    return next(i for i, s in enumerate(scenes) if s.start <= t < s.end)
