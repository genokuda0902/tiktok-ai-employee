"""Zero-cost subtle ambient bed contract for image-slide videos.

The bed is synthesized with FFmpeg anoisesrc, so it needs no licensed music
asset or paid service. It must stay quiet under Japanese narration and never
changes release policy: human approval/manual posting remain mandatory.
"""


def ambient_bed_filter(duration: float, sample_rate: int = 48000) -> str:
    if duration <= 0 or duration > 180:
        raise ValueError("duration must be in (0, 180]")
    if sample_rate != 48000:
        raise ValueError("ambient bed requires 48 kHz")
    return (
        f"anoisesrc=color=pink:amplitude=0.015:sample_rate={sample_rate}:duration={duration:.3f},"
        "highpass=f=180,lowpass=f=1800,volume=0.10"
    )


def mix_contract(width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("ambient-bed route requires 1080x1920")
    return {
        "bed_weight": 0.22,
        "narration_weight": 1.0,
        "zero_cost": True,
        "external_music_asset_required": False,
        "human_approval_required": True,
        "auto_post": False,
    }
