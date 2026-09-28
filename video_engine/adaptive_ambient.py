"""Zero-cost narration-aware ambient bed for image-slide videos."""

BED_MIX_WEIGHT = 0.10


def adaptive_ambient_filter(duration: float, sample_rate: int = 48000) -> str:
    if duration <= 0 or duration > 180:
        raise ValueError("duration must be in (0, 180]")
    if sample_rate != 48000:
        raise ValueError("adaptive ambient requires 48 kHz")
    return (
        f"anoisesrc=color=pink:amplitude=0.015:sample_rate={sample_rate}:duration={duration:.3f},"
        "highpass=f=180,lowpass=f=1800,volume=0.10[bed];"
        "[narration]asplit=2[narr][key];"
        "[bed][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=250[ducked];"
        f"[narr][ducked]amix=inputs=2:weights='1 {BED_MIX_WEIGHT:.2f}':normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=7[aout]"
    )


def adaptive_ambient_contract(width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("adaptive ambient route requires 1080x1920")
    return {
        "zero_cost": True,
        "preserve_video": True,
        "preserve_burned_captions": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "changes_caption_copy": False,
        "bed_mix_weight": BED_MIX_WEIGHT,
    }
