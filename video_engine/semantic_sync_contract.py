"""Zero-cost semantic-sync contract for image-slide TikTok videos.

Keeps image intent, narration and burned caption aligned from one scene source.
No posting or paid services are invoked here.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    image_intent: str
    narration: str
    caption: str
    duration_s: float


def validate_scene(scene: Scene) -> None:
    if not scene.image_intent.strip():
        raise ValueError("image_intent is required")
    if not scene.narration.strip():
        raise ValueError("narration is required")
    if not scene.caption.strip():
        raise ValueError("caption is required")
    if not (1.0 <= scene.duration_s <= 4.5):
        raise ValueError("duration_s must be 1.0..4.5")
    # Phrase captions must remain short enough for mobile reading.
    if len(scene.caption) > 28:
        raise ValueError("caption exceeds 28 characters")


def validate_story(scenes: list[Scene]) -> None:
    if not (8 <= len(scenes) <= 12):
        raise ValueError("story must contain 8..12 scenes")
    for scene in scenes:
        validate_scene(scene)
    total = sum(s.duration_s for s in scenes)
    if not (12.0 <= total <= 35.0):
        raise ValueError("story duration must be 12..35 seconds")
