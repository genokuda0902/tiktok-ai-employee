"""Zero-cost finishing filters for image-slide TikTok masters.

This module targets gradient/compression banding without changing narration,
caption copy, timing, or the human-approval/manual-posting contract.
"""


def finishing_filter(width: int = 1080, height: int = 1920) -> str:
    """Return a conservative FFmpeg filter chain for final portrait masters."""
    if (width, height) != (1080, 1920):
        raise ValueError("image-slide finishing requires 1080x1920")
    return (
        "deband=1thr=0.018:2thr=0.018:3thr=0.018:4thr=0.018:range=12:blur=true,"
        "unsharp=5:5:0.18:5:5:0"
    )


def finishing_contract(width: int = 1080, height: int = 1920) -> dict:
    """Fail closed and preserve the project's release-safety constraints."""
    chain = finishing_filter(width, height)
    return {
        "width": width,
        "height": height,
        "filter": chain,
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
        "changes_audio": False,
        "changes_caption_copy": False,
    }
