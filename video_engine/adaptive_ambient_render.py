"""Zero-cost adaptive ambient render plan for the image-slide route.

Keeps the picture/captions untouched, synthesizes a quiet band-limited pink-noise
bed locally, ducks it under narration, and preserves manual human approval.
"""


def ffmpeg_filter(duration: float, width: int = 1080, height: int = 1920) -> str:
    if width != 1080 or height != 1920:
        raise ValueError("delivery geometry must be 1080x1920")
    if not (1.0 <= duration <= 180.0):
        raise ValueError("duration out of supported range")
    return (
        "[1:a]highpass=f=180,lowpass=f=1800,volume=0.10[bed];"
        "[bed][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=250[duck];"
        "[0:a][duck]amix=inputs=2:weights='1 0.10':normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=7[a]"
    )


def release_contract() -> dict:
    return {
        "zero_cost": True,
        "synthesized_bed_only": True,
        "preserve_video_and_burned_captions": True,
        "audio_rate": 48000,
        "audio_channels": 2,
        "human_approval_required": True,
        "auto_post": False,
    }
