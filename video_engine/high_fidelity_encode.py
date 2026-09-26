"""Zero-cost high-fidelity delivery encode for image-slide TikTok masters.

Keeps the approved audio stream bit-for-bit while re-encoding only video with a
conservative H.264 CRF target suitable for 1080x1920 image-slide masters.
Human quality/rights approval and manual posting remain mandatory.
"""

CRF = 16
PRESET = "slow"
PIX_FMT = "yuv420p"
PROFILE = "high"
LEVEL = "4.1"


def encode_contract(width: int = 1080, height: int = 1920, fps: int = 30) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery master must be 1080x1920")
    if fps != 30:
        raise ValueError("delivery master must be 30 fps")
    return {
        "video_codec": "libx264",
        "preset": PRESET,
        "crf": CRF,
        "pix_fmt": PIX_FMT,
        "profile": PROFILE,
        "level": LEVEL,
        "movflags": "+faststart",
        "audio_codec": "copy",
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
    }


def ffmpeg_args() -> list[str]:
    c = encode_contract()
    return [
        "-c:v", c["video_codec"], "-preset", c["preset"], "-crf", str(c["crf"]),
        "-pix_fmt", c["pix_fmt"], "-profile:v", c["profile"], "-level", c["level"],
        "-movflags", c["movflags"], "-c:a", c["audio_codec"],
    ]
