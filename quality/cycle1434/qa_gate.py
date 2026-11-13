"""Fail-closed quality gate for 10 genre review renders. No publish authorization."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    decoded: bool
    width: int
    height: int
    japanese_narration_verified: bool
    captions_synchronized: bool
    assets_approved: bool
    employee_approved: bool

def assess(e: Evidence) -> dict:
    issues = []
    if not e.decoded: issues.append("decode_failed")
    if (e.width, e.height) != (1080, 1920): issues.append("resolution_mismatch")
    if not e.japanese_narration_verified: issues.append("narration_missing")
    if not e.captions_synchronized: issues.append("captions_not_synchronized")
    if not e.assets_approved: issues.append("assets_not_approved")
    if not e.employee_approved: issues.append("employee_approval_missing")
    return {"posting_allowed": not issues, "issues": issues}
