"""Cycle130 clean-native slide specification.

Zero-cost reusable structure for 10 genres. Rendering remains local/CI; this module
only defines fail-closed layout constraints and scene validation.
"""
from dataclasses import dataclass

WIDTH, HEIGHT = 1080, 1920
SAFE_X = 70
CAPTION_TOP = 1580
CAPTION_BOTTOM = 1770

@dataclass(frozen=True)
class Scene:
    kicker: str
    title: str
    subtitle: str
    caption: str
    duration: float = 1.3625

def validate_scene(scene: Scene) -> None:
    if not scene.title.strip() or not scene.caption.strip():
        raise ValueError("title/caption required")
    if not 0.8 <= scene.duration <= 3.0:
        raise ValueError("scene duration out of range")
    if len(scene.title) > 18:
        raise ValueError("title too long for one-message layout")
    if len(scene.caption) > 32:
        raise ValueError("caption too long for mobile legibility")

def validate_story(scenes: list[Scene]) -> None:
    if not 8 <= len(scenes) <= 12:
        raise ValueError("story must contain 8-12 scenes")
    for scene in scenes:
        validate_scene(scene)
