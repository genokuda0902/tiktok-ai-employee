"""Zero-cost conservative detail restoration for image-slide TikTok videos.

Applies luma-only sharpening after compositing/caption burn-in to recover a small
amount of perceived detail lost during scaling/encoding. It is intentionally
bounded to avoid halos and oversharpening. Human quality/rights approval remains
mandatory before manual posting.
"""


def ffmpeg_filter(luma_amount: float = 0.28) -> str:
    """Return a bounded FFmpeg unsharp filter for 1080x1920 image-slide output."""
    if not (0.0 <= luma_amount <= 0.40):
        raise ValueError("luma_amount must be between 0 and 0.40")
    return f"unsharp=5:5:{luma_amount}:3:3:0.0"
