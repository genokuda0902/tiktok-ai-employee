"""Zero-cost hook-latency correction for image-slide TikTok masters.

Removes only measured leading narration silence so the first spoken hook starts
immediately, while preserving the approved visual stream/caption copy and the
delivery duration. Human approval and manual posting remain required.
"""

MAX_LEADING_SILENCE = 0.75


def hook_latency_contract(leading_silence: float, duration: float = 20.0) -> dict:
    if duration <= 0:
        raise ValueError("duration must be positive")
    if leading_silence < 0 or leading_silence > MAX_LEADING_SILENCE:
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


def ffmpeg_audio_filter(leading_silence: float = 0.44, duration: float = 20.0) -> str:
    """Return the deterministic filter after silence has been measured.

    0.44 s is the measured cycle40 baseline (silencedetect -38 dB, d=0.25),
    replacing the older 0.42 s provisional default.
    """
    return hook_latency_contract(leading_silence, duration)["audio_filter"]
