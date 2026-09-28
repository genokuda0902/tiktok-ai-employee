"""Finalize adaptive ambient audio without shortening the portrait video."""

def adaptive_finalize_filter(duration: float, width: int = 1080, height: int = 1920) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if not 1.0 <= duration <= 180.0:
        raise ValueError("duration out of supported range")
    return (
        "[1:a]highpass=f=180,lowpass=f=1800,volume=0.10[bed];"
        "[bed][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=250[duck];"
        "[0:a][duck]amix=inputs=2:weights='1 0.10':normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=7,"
        f"apad=pad_dur=0.1,atrim=duration={duration:.6f}[a]"
    )

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "video_stream_copy": True,
        "preserve_burned_captions": True,
        "audio_rate": 48000,
        "audio_channels": 2,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
