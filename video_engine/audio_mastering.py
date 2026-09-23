"""Zero-cost narration mastering for image-slide TikTok videos.

Keeps the visual route unchanged and improves speech intelligibility using only
FFmpeg built-in filters. This does not synthesize or replace narration and does
not imply publish readiness; human review remains mandatory.
"""


def narration_master_filter(sample_rate: int = 48000, channels: int = 2) -> str:
    """Return a deterministic, genre-independent Japanese narration master chain."""
    if sample_rate != 48000:
        raise ValueError("narration mastering requires 48 kHz audio")
    if channels != 2:
        raise ValueError("narration mastering requires stereo audio")
    return (
        "highpass=f=80,"
        "lowpass=f=12000,"
        "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120:makeup=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=7"
    )


def mastering_contract(width: int, height: int, sample_rate: int, channels: int) -> dict:
    """Fail closed unless the shared 10-genre delivery contract is satisfied."""
    if (width, height) != (1080, 1920):
        raise ValueError("mastered image-slide videos require 1080x1920")
    audio_filter = narration_master_filter(sample_rate, channels)
    return {
        "width": width,
        "height": height,
        "sample_rate": sample_rate,
        "channels": channels,
        "audio_filter": audio_filter,
        "human_approval_required": True,
        "auto_post": False,
    }
