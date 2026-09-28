"""Zero-cost slide-first storyboard contract for TikTok image videos.

Each scene is a finished 1080x1920 image card. Motion/audio/captions are applied only
after the visual story is understandable from the cards themselves.
"""
from dataclasses import dataclass
from typing import Sequence

BEATS = ("hook", "before", "solution", "demo", "after", "cta")

@dataclass(frozen=True)
class SlideCard:
    beat: str
    image_path: str
    headline: str
    narration: str
    caption: str
    rights_approved: bool
    quality_approved: bool


def validate_slide_first(cards: Sequence[SlideCard], width: int = 1080, height: int = 1920) -> None:
    if (width, height) != (1080, 1920):
        raise ValueError("slide-first master must be 1080x1920")
    if tuple(c.beat for c in cards) != BEATS:
        raise ValueError("six semantic beats required in fixed order")
    if len({c.image_path for c in cards}) != len(cards):
        raise ValueError("each beat requires a distinct finished image")
    for c in cards:
        if not all((c.image_path, c.headline, c.narration, c.caption)):
            raise ValueError("image/headline/narration/caption are required")
        if not c.rights_approved or not c.quality_approved:
            raise ValueError("rights and human quality approval are required")
