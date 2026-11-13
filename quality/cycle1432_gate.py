"""Reusable quality gate for 10 genre image-first videos. Review only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class VideoEvidence:
    video_codec: str
    width: int
    height: int
    duration_seconds: float
    audio_codec: str
    japanese_narration_verified: bool
    captions_synced: bool
    assets_approved: bool
    employee_approved: bool
    decode_passed: bool

def publication_ready(e: VideoEvidence) -> bool:
    return (e.video_codec == "h264" and e.width == 1080
            and e.height == 1920 and 10 <= e.duration_seconds <= 60
            and e.audio_codec == "aac" and e.japanese_narration_verified
            and e.captions_synced and e.assets_approved
            and e.employee_approved and e.decode_passed)
