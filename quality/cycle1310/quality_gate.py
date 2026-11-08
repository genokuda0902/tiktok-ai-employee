"""Fail-closed checks for review-only video outputs (all genres)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    video_decodes: bool
    vertical_1080p: bool
    japanese_narration_verified: bool
    speech_aligned_captions_verified: bool
    assets_approved: bool
    privacy_reviewed: bool
    employee_approved: bool

def can_publish(e: Evidence) -> bool:
    return all(vars(e).values())

def test_silent_video_never_passes():
    e = Evidence(True, True, False, False, True, True, True)
    assert not can_publish(e)

def test_unapproved_assets_never_pass():
    e = Evidence(True, True, True, True, False, True, True)
    assert not can_publish(e)

def test_all_evidence_required():
    e = Evidence(True, True, True, True, True, True, True)
    assert can_publish(e)

if __name__ == "__main__":
    test_silent_video_never_passes()
    test_unapproved_assets_never_pass()
    test_all_evidence_required()
    print("3 tests passed")
