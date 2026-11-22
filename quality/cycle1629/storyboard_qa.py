"""Review-only storyboard QA: never infer Japanese speech from graphics or a track."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewEvidence:
    width: int
    height: int
    duration_seconds: float
    scene_count: int
    audio_stream_present: bool
    japanese_speech_verified: bool
    captions_synced_verified: bool
    assets_approved: bool
    employee_approved: bool

def assess(e: ReviewEvidence) -> dict:
    failures = []
    if (e.width, e.height) != (1080, 1920):
        failures.append("target_resolution_not_met")
    if e.duration_seconds <= 0 or e.scene_count < 3:
        failures.append("storyboard_incomplete")
    if not e.audio_stream_present:
        failures.append("audio_missing")
    if not e.japanese_speech_verified:
        failures.append("japanese_speech_unverified")
    if not e.captions_synced_verified:
        failures.append("speech_caption_sync_unverified")
    if not e.assets_approved:
        failures.append("asset_approval_missing")
    if not e.employee_approved:
        failures.append("employee_approval_missing")
    return {"publication_approved": not failures, "failures": failures}
