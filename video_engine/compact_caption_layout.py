"""Fail-closed compact caption layout contract for portrait image-slide videos.

Keeps captions readable without covering a large portion of the source image.
Rendering remains subject to human quality/rights approval; this module does not post.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class CompactCaptionLayout:
    canvas_width: int = 1080
    canvas_height: int = 1920
    card_x: int = 120
    card_y: int = 1365
    card_width: int = 840
    card_height: int = 120
    max_chars: int = 18

    def validate(self) -> None:
        if (self.canvas_width, self.canvas_height) != (1080, 1920):
            raise ValueError("portrait output must be 1080x1920")
        if min(self.card_x, self.card_y, self.card_width, self.card_height) < 0:
            raise ValueError("caption geometry must be non-negative")
        if self.card_x + self.card_width > self.canvas_width:
            raise ValueError("caption card exceeds canvas width")
        if self.card_y + self.card_height > self.canvas_height:
            raise ValueError("caption card exceeds canvas height")
        if self.card_height > 160:
            raise ValueError("caption card is too tall and obscures source imagery")
        if not 1 <= self.max_chars <= 22:
            raise ValueError("caption phrase length must stay short")


def validate_phrase(text: str, layout: CompactCaptionLayout | None = None) -> str:
    layout = layout or CompactCaptionLayout()
    layout.validate()
    phrase = text.strip()
    if not phrase:
        raise ValueError("caption phrase is required")
    if len(phrase) > layout.max_chars:
        raise ValueError("caption phrase exceeds compact-card limit")
    return phrase
