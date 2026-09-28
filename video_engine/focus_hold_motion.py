"""Zero-cost bounded focus-hold motion for portrait image-slide renders.

Adds very subtle continuous pan/zoom energy without changing narration or caption
copy. Release remains human-approved and manual-post only.
"""


def ffmpeg_filter(width: int = 1080, height: int = 1920) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("focus-hold requires 1080x1920")
    return (
        "scale=1092:1941:flags=lanczos,"
        "crop=1080:1920:"
        "x='6+3*sin(2*PI*t/4.2)':"
        "y='10+4*cos(2*PI*t/5.1)'"
    )


def release_policy() -> dict:
    return {
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "width": 1080,
        "height": 1920,
    }
