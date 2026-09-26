"""Zero-cost final deband pass for already-sharpened image-slide masters."""


def ffmpeg_filter(width: int = 1080, height: int = 1920) -> str:
    """Reduce gradient/compression banding without applying a second sharpen pass."""
    if (width, height) != (1080, 1920):
        raise ValueError("deband finish requires 1080x1920")
    return "deband=1thr=0.018:2thr=0.018:3thr=0.018:4thr=0.018:range=12:blur=true"


def safety_contract() -> dict:
    return {
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "auto_post": False,
        "second_sharpen": False,
    }
