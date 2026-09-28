"""Fail-closed mobile delivery contract for rendered TikTok MP4 metadata."""
from dataclasses import dataclass

@dataclass(frozen=True)
class DeliveryMeta:
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: str
    audio_rate: int
    audio_channels: int
    moov_before_mdat: bool
    max_keyframe_gap_s: float

def validate_mobile_delivery(m: DeliveryMeta) -> None:
    errors = []
    if (m.width, m.height) != (1080, 1920): errors.append("resolution")
    if m.video_codec != "h264": errors.append("video_codec")
    if abs(m.fps - 30.0) > 0.01: errors.append("fps")
    if m.audio_codec != "aac": errors.append("audio_codec")
    if m.audio_rate != 48000 or m.audio_channels != 2: errors.append("audio_format")
    if not m.moov_before_mdat: errors.append("faststart")
    if m.max_keyframe_gap_s > 1.05: errors.append("keyframe_gap")
    if errors:
        raise ValueError("mobile delivery contract failed: " + ",".join(errors))
