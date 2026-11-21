"""Review-only QA gate shared by all content genres. No upload/post action."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    video_decodes: bool
    vertical_resolution_ok: bool
    japanese_narration_verified: bool
    timed_captions_verified: bool
    assets_approved: bool
    privacy_reviewed: bool
    employee_approved: bool

def posting_allowed(evidence: Evidence) -> bool:
    return all(vars(evidence).values())

if __name__ == "__main__":
    sample = Evidence(True, True, False, False, True, True, False)
    assert not posting_allowed(sample)
    assert posting_allowed(Evidence(*([True] * 7)))
    assert all(not posting_allowed(Evidence(*[j != i for j in range(7)])) for i in range(7))
    print("PASS: 9 fail-closed checks")
