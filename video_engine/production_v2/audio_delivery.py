"""Zero-cost delivery-audio contract for review-only TikTok masters."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AudioDelivery:
    sample_rate: int = 48000
    channels: int = 2
    integrated_lufs: float = -16.0
    true_peak_dbtp: float = -1.5
    lra: float = 7.0

    def validate(self):
        if self.sample_rate != 48000 or self.channels != 2:
            raise ValueError("delivery audio must be 48 kHz stereo")
        if not (-18.0 <= self.integrated_lufs <= -14.0):
            raise ValueError("integrated loudness outside review target")
        if self.true_peak_dbtp > -1.0:
            raise ValueError("true peak unsafe")
        return self

def ffmpeg_filter(contract=AudioDelivery()):
    c=contract.validate()
    return (
        "pan=stereo|c0=c0|c1=c0,"
        f"loudnorm=I={c.integrated_lufs:g}:TP={c.true_peak_dbtp:g}:LRA={c.lra:g}"
    )

def release_policy():
    return {
        "zero_cost": True,
        "preserve_video": True,
        "preserve_burned_captions": True,
        "human_pronunciation_review_required": True,
        "quality_approved": False,
        "manual_post_only": True,
        "auto_post": False,
    }
