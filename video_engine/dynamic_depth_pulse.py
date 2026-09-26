"""Zero-cost subtle luminance-depth pulse for image-slide TikTok videos.

Designed to be genre-independent and applied after captions are burned in.
Human quality/rights approval remains mandatory before manual posting.
"""


def ffmpeg_filter(contrast_amount: float = 0.025, brightness_amount: float = 0.006) -> str:
    if not (0.0 <= contrast_amount <= 0.05):
        raise ValueError("contrast_amount must be between 0 and 0.05")
    if not (0.0 <= brightness_amount <= 0.015):
        raise ValueError("brightness_amount must be between 0 and 0.015")
    return (
        "eq="
        f"contrast='1+{contrast_amount}*sin(2*PI*t/3.8)':"
        f"brightness='{brightness_amount}*sin(2*PI*t/4.6)'"
    )
