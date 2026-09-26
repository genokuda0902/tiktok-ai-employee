"""Fail-closed hook evidence contract for Production v2.

Keeps the first 1.5 seconds result-first without approving content or enabling posting.
"""
from dataclasses import dataclass

ALLOWED_EVIDENCE = {"before_after", "screen_demo", "measured_result", "comparison", "work_scene"}

@dataclass(frozen=True)
class HookEvidence:
    duration_s: float
    headline: str
    evidence_type: str
    has_numeric_or_visual_result: bool
    rights_approved: bool
    contains_personal_data: bool = False

def validate_hook(hook: HookEvidence) -> None:
    if not (0.4 <= hook.duration_s <= 1.5):
        raise ValueError("hook must resolve within 0.4-1.5s")
    if len(hook.headline.strip()) < 4:
        raise ValueError("hook headline too weak")
    if hook.evidence_type not in ALLOWED_EVIDENCE:
        raise ValueError("generic/placeholder hook evidence rejected")
    if not hook.has_numeric_or_visual_result:
        raise ValueError("result-first evidence required")
    if not hook.rights_approved:
        raise ValueError("unapproved asset rights")
    if hook.contains_personal_data:
        raise ValueError("personal data rejected")
