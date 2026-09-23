"""Zero-cost hook-latency correction for image-slide TikTok masters.

Removes only measured leading narration silence so the first spoken hook starts
immediately, while preserving the approved visual stream/caption copy and the
20-second delivery duration. Human approval and manual posting remain required.
"""


def hook_latency_contract(leading_silence: float, duration: float = 20.0) -> dict:
    if duration <= 0:
        raise ValueError("duration must be positive")
    if leading_silence < 0 or leading_silence > 0.75:
        raise ValueError("leading silence correction must be measured and <= 0.75s")
    return {
        "leading_silence": float(leading_silence),
        "duration": float(duration),
        "audio_filter": (
            f"atrim=start={leading_silence:.2f},asetpts=PTS-STARTPTS,"
            f"apad=pad_dur={leading_silence:.2f},atrim=duration={duration:g}"
        ),
        "video_copy": True,
        "caption_copy_unchanged": True,
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
    }


def ffmpeg_audio_filter(leading_silence: float = 0.42, duration: float = 20.0) -> str:
    """Return the deterministic audio filter after silence has been measured."""
    return hook_latency_contract(leading_silence, duration)["audio_filter"]
