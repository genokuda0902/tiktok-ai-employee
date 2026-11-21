"""Fail-closed review gate shared by all ten genres. Never infer spoken Japanese from an AAC stream."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    video_decodes: bool
    japanese_narration_verified: bool
    captions_synced_verified: bool
    assets_approved: bool
    employee_approved: bool

def publication_allowed(e: Evidence) -> bool:
    return all((e.video_decodes, e.japanese_narration_verified,
                e.captions_synced_verified, e.assets_approved,
                e.employee_approved))

def test_silent_video_rejected():
    assert not publication_allowed(Evidence(True, False, False, True, True))

def test_missing_approval_rejected():
    assert not publication_allowed(Evidence(True, True, True, True, False))

def test_complete_evidence_passes():
    assert publication_allowed(Evidence(True, True, True, True, True))
