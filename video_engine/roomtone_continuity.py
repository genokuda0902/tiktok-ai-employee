"""Zero-cost low-level room-tone continuity for image-first TikTok videos.

Adds a synthesized, band-limited pink-noise floor under narration so pauses do not
collapse into absolute digital silence. No external music/media asset is required.
Human quality/rights approval and manual posting remain mandatory.
"""

def ffmpeg_filter(duration_s: float, width: int = 1080, height: int = 1920,
                  sample_rate: int = 48000, floor_gain: float = 0.0035) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if sample_rate != 48000:
        raise ValueError("delivery audio must be 48kHz")
    if duration_s <= 0:
        raise ValueError("duration must be positive")
    if not 0.001 <= floor_gain <= 0.006:
        raise ValueError("room-tone floor must remain subtle")
    return (
        f"anoisesrc=color=pink:sample_rate={sample_rate}:duration={duration_s:.6f},"
        f"highpass=f=180,lowpass=f=1800,volume={floor_gain:.4f}[room];"
        "[0:a][room]amix=inputs=2:duration=first:weights='1 1':normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=7[aout]"
    )

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "synthesized_audio_only": True,
        "external_music_asset_required": False,
        "video_stream_passthrough": True,
        "preserve_burned_captions": True,
        "human_quality_review_required": True,
        "human_rights_review_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "claims_publish_ready": False,
    }
