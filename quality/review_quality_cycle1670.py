"""Review-only video quality contract for ten genres. No publication authorization."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewEvidence:
    has_video: bool
    has_real_japanese_narration: bool
    captions_synced_to_speech: bool
    licensed_assets: bool
    employee_approved: bool
    actual_operation_recording: bool

def can_publish(e: ReviewEvidence) -> bool:
    return all((e.has_video, e.has_real_japanese_narration,
                e.captions_synced_to_speech, e.licensed_assets,
                e.employee_approved))

def shortcomings(e: ReviewEvidence) -> list[str]:
    checks = {
        "video_missing": e.has_video,
        "japanese_narration_missing": e.has_real_japanese_narration,
        "speech_caption_sync_missing": e.captions_synced_to_speech,
        "asset_rights_unverified": e.licensed_assets,
        "employee_approval_missing": e.employee_approved,
        "actual_operation_not_recorded": e.actual_operation_recording,
    }
    return [name for name, passed in checks.items() if not passed]
