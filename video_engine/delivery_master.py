"""Zero-cost high-fidelity delivery settings for portrait image-slide masters.

Keeps the approved image/audio/caption content unchanged while producing a
TikTok-friendly H.264/AAC MP4 with fast-start metadata. Human approval and
manual posting remain mandatory.
"""


def delivery_contract(width: int = 1080, height: int = 1920, fps: int = 30) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery master requires 1080x1920")
    if fps != 30:
        raise ValueError("delivery master requires 30 fps")
    return {
        "width": width,
        "height": height,
        "fps": fps,
        "video_codec": "libx264",
        "preset": "slow",
        "crf": 15,
        "profile": "high",
        "level": "4.1",
        "pixel_format": "yuv420p",
        "audio_codec": "aac",
        "audio_bitrate": "192k",
        "audio_rate": 48000,
        "audio_channels": 2,
        "movflags": "+faststart",
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
        "changes_audio_copy": False,
        "changes_caption_copy": False,
    }


def ffmpeg_args() -> list[str]:
    c = delivery_contract()
    return [
        "-c:v", c["video_codec"], "-preset", c["preset"], "-crf", str(c["crf"]),
        "-profile:v", c["profile"], "-level", c["level"], "-pix_fmt", c["pixel_format"],
        "-r", str(c["fps"]), "-c:a", c["audio_codec"], "-b:a", c["audio_bitrate"],
        "-ar", str(c["audio_rate"]), "-ac", str(c["audio_channels"]),
        "-movflags", c["movflags"],
    ]
