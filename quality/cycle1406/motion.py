"""Reusable scene motion parameters for review-only videos (no external assets)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Motion:
    reveal: float
    progress: float
    cursor_row: int

def frame_motion(frame: int, fps: int, scene_seconds: int, scene_index: int, total_scenes: int) -> Motion:
    if min(fps, scene_seconds, total_scenes) <= 0 or frame < 0 or not 0 <= scene_index < total_scenes:
        raise ValueError("invalid timing")
    scene_frames = fps * scene_seconds
    if frame >= scene_frames:
        raise ValueError("frame exceeds scene")
    reveal = min(1.0, frame / max(1, round(fps * 0.7)))
    progress = (scene_index * scene_frames + frame + 1) / (total_scenes * scene_frames)
    row = min(2, (frame * 3) // scene_frames)
    return Motion(reveal, progress, row)
