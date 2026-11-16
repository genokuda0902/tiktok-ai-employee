"""Common TikTok safe-zone and narration approval gate. Reimplementation, not v33 source."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Review:
    width: int
    height: int
    duration: float
    audio_codec: str | None
    japanese_narration_verified: bool
    captions_synced_verified: bool
    approved_assets: bool

def review_video(r: Review) -> dict:
    issues = []
    if (r.width, r.height) not in ((720, 1280), (1080, 1920)):
        issues.append("vertical_resolution")
    if not 8 <= r.duration <= 60:
        issues.append("duration")
    if not r.audio_codec:
        issues.append("missing_audio_track")
    if not r.japanese_narration_verified:
        issues.append("japanese_narration_unverified")
    if not r.captions_synced_verified:
        issues.append("caption_sync_unverified")
    if not r.approved_assets:
        issues.append("assets_unapproved")
    return {"approved_for_posting": not issues, "issues": issues}
