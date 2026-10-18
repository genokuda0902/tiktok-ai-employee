"""Cycle 666: genre-neutral hook + subtitle safe-area contract (stdlib only).

This is the reusable contract, not the complete MP4 renderer.
The complete renderer, local tests and media assets are delivered in the cycle ZIP.
"""
from dataclasses import dataclass
from typing import Sequence

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SAFE_CAPTION_BOUNDS = (50, 1430, 900, 1680)
PUBLICATION = "HUMAN_REVIEW / NOT_APPROVED"

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    spoken_text: str
    image_path: str

def validate_scenes(scenes: Sequence[Scene], genre_names: Sequence[str]) -> None:
    if len(genre_names) != 10 or len(set(genre_names)) != 10:
        raise ValueError("Ten distinct genres are required")
    if not scenes:
        raise ValueError("At least one scene is required")
    if abs(scenes[0].start) > 0.0001:
        raise ValueError("Timeline must start at zero")
    for i, scene in enumerate(scenes):
        if scene.end <= scene.start or not scene.spoken_text.strip():
            raise ValueError(f"Invalid scene {i}")
        if not scene.image_path:
            raise ValueError(f"Missing image for scene {i}")
        if i and abs(scenes[i - 1].end - scene.start) > 0.001:
            raise ValueError(f"Timeline gap/overlap at scene {i}")

def validate_caption_bbox(box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    sx0, sy0, sx1, sy1 = SAFE_CAPTION_BOUNDS
    if not (sx0 <= x0 < x1 <= sx1 and sy0 <= y0 < y1 <= sy1):
        raise ValueError("Caption overlaps the mobile UI safe-area boundary")

def opening_hook_label(topic: str) -> str:
    if not topic.strip():
        raise ValueError("Topic required")
    return f"これ、{topic.strip()}？"
