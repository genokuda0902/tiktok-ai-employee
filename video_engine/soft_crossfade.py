"""Zero-cost soft crossfade contract for image-first TikTok slides."""

from __future__ import annotations


def crossfade_contract(width: int = 1080, height: int = 1920, duration: float = 0.12) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if not 0.08 <= duration <= 0.18:
        raise ValueError("crossfade must stay subtle (80-180 ms)")
    return {
        "width": width,
        "height": height,
        "transition": "fade",
        "duration_seconds": duration,
        "zero_cost": True,
        "preserve_narration": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }


def xfade_filter(offset: float, duration: float = 0.12) -> str:
    if offset < duration:
        raise ValueError("offset must be after transition duration")
    crossfade_contract(duration=duration)
    return f"xfade=transition=fade:duration={duration:.3f}:offset={offset:.3f}"
