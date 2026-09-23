"""Zero-cost subtle focus vignette for portrait image-slide videos.

The effect is deliberately bounded: it darkens only the outer frame slightly so
central image/UI content and burned Japanese captions remain visually dominant.
It does not alter narration, caption copy, timing, or posting policy.
"""


def ffmpeg_filter(width: int = 1080, height: int = 1920, strength: float = 0.10) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery geometry must be 1080x1920")
    if not 0.04 <= strength <= 0.12:
        raise ValueError("focus vignette must remain subtle")
    # FFmpeg vignette angle: PI/2 is strongest; values nearer PI/2 darken edges.
    angle = 1.57079632679 - strength
    return f"vignette=PI/4+{strength:.3f}:eval=frame"


def safety_contract() -> dict:
    return {
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "preserve_timing": True,
        "human_approval_required": True,
        "auto_post": False,
        "max_strength": 0.12,
    }
