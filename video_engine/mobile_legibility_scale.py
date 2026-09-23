"""Zero-cost mobile legibility finishing for portrait image-slide videos.

Applies a tiny bounded center scale to make dense screenshots/cards more readable on
phones without changing timing, narration, captions, or approval policy.
"""
from dataclasses import dataclass

MIN_SCALE = 1.0
MAX_SCALE = 1.03

@dataclass(frozen=True)
class LegibilityScale:
    scale: float = 1.018


def validate(config: LegibilityScale) -> None:
    if not (MIN_SCALE <= config.scale <= MAX_SCALE):
        raise ValueError("legibility scale must stay within 1.00..1.03")


def ffmpeg_filter(config: LegibilityScale = LegibilityScale()) -> str:
    validate(config)
    s = config.scale
    return (
        f"scale=ceil(iw*{s:.4f}/2)*2:ceil(ih*{s:.4f}/2)*2:flags=lanczos,"
        "crop=1080:1920:(iw-1080)/2:(ih-1920)/2"
    )


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
