"""Genre-independent keyword emphasis for image-first TikTok renders.

This module only builds a conservative FFmpeg drawtext filter. It does not
publish media. Human quality/rights approval remains mandatory.
"""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class KeywordBeat:
    text: str
    start: float
    end: float


def validate_beats(beats: Iterable[KeywordBeat], duration: float) -> list[KeywordBeat]:
    items = list(beats)
    if duration <= 0 or not items:
        raise ValueError("duration and at least one keyword beat are required")
    last_end = 0.0
    for beat in items:
        if not beat.text.strip() or len(beat.text) > 12:
            raise ValueError("keyword must contain 1-12 characters")
        if beat.start < 0 or beat.end <= beat.start or beat.end > duration:
            raise ValueError("keyword timing is outside the video")
        if beat.start < last_end:
            raise ValueError("keyword beats must not overlap")
        last_end = beat.end
    return items


def build_drawtext_filters(beats: Iterable[KeywordBeat], duration: float, fontfile: str) -> str:
    """Return safe-zone drawtext filters for short semantic keywords.

    The y=1320 placement keeps the emphasis above the lower caption/progress
    area used by the current image-slide renderer. Text is intentionally short
    so the overlay supplements rather than replaces synchronized captions.
    """
    items = validate_beats(beats, duration)
    if not fontfile:
        raise ValueError("fontfile is required")
    filters = []
    for beat in items:
        text = beat.text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        filters.append(
            "drawtext="
            f"fontfile='{fontfile}':text='{text}':"
            "fontcolor=white:fontsize=72:borderw=5:bordercolor=black@0.85:"
            "box=1:boxcolor=0x111111@0.72:boxborderw=18:"
            "x=(w-text_w)/2:y=1320:"
            f"enable='between(t,{beat.start:.3f},{beat.end:.3f})'"
        )
    return ",".join(filters)
