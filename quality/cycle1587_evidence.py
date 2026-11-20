"""Fail-closed review evidence gate, reusable for ten genres."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    video_decodes: bool
    japanese_narration_verified: bool
    spoken_caption_sync_verified: bool
    asset_rights_approved: bool
    employee_approved: bool

def publication_approved(e: Evidence) -> bool:
    return all((e.video_decodes, e.japanese_narration_verified,
                e.spoken_caption_sync_verified, e.asset_rights_approved,
                e.employee_approved))
