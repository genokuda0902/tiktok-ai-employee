"""Phrase-caption contract for image-first TikTok videos.

Keeps captions short, readable and inside a conservative vertical safe area.
This module is genre-independent and zero-cost. It does not auto-post and does
not replace human rights/quality approval.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhraseCaption:
    start: float
    end: float
    text: str


def validate_caption(caption: PhraseCaption, *, max_chars: int = 22) -> None:
    if caption.start < 0 or caption.end <= caption.start:
        raise ValueError("invalid caption timing")
    if not caption.text.strip():
        raise ValueError("caption text is required")
    lines = caption.text.split("\\N")
    if len(lines) > 2:
        raise ValueError("caption must use at most two lines")
    if any(len(line) > max_chars for line in lines):
        raise ValueError("caption line is too long")


def validate_sequence(captions: list[PhraseCaption], duration: float) -> None:
    if duration <= 0:
        raise ValueError("duration must be positive")
    previous_end = 0.0
    for caption in captions:
        validate_caption(caption)
        if caption.start < previous_end:
            raise ValueError("captions must not overlap")
        if caption.end > duration + 1e-6:
            raise ValueError("caption exceeds video duration")
        previous_end = caption.end


def ass_safe_margin_v(frame_height: int = 1920) -> int:
    if frame_height <= 0:
        raise ValueError("frame_height must be positive")
    return round(frame_height * 0.12)
