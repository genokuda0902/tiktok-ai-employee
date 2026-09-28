"""Zero-cost, conservative narration de-essing for the image-slide route.

This stage changes audio only. It preserves the rendered video/captions and keeps
release behind human quality/rights approval; it never posts to TikTok.
"""


def deesser_filter(intensity: float = 0.15, max_deessing: float = 0.25, frequency: float = 0.60) -> str:
    if not (0.0 <= intensity <= 0.20):
        raise ValueError("intensity must stay conservative (0..0.20)")
    if not (0.0 <= max_deessing <= 0.30):
        raise ValueError("max_deessing must stay conservative (0..0.30)")
    if not (0.45 <= frequency <= 0.75):
        raise ValueError("frequency must stay in the speech-sibilance guard band")
    return f"deesser=i={intensity:.2f}:m={max_deessing:.2f}:f={frequency:.2f}"


def release_contract(width: int = 1080, height: int = 1920, sample_rate: int = 48000, channels: int = 2) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if (sample_rate, channels) != (48000, 2):
        raise ValueError("delivery audio must be 48kHz stereo")
    return {
        "zero_cost": True,
        "video_stream_passthrough": True,
        "caption_copy_preserved": True,
        "human_approval_required": True,
        "auto_post": False,
        "claims_publish_ready": False,
    }
