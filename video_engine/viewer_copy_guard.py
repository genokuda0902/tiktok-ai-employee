"""Fail closed when internal production labels leak into viewer-facing copy.

These tokens are useful in story planning but should not be baked into TikTok frames.
No posting or paid services are performed here.
"""
import re
from typing import Iterable

FORBIDDEN_ROLE_LABELS = {
    "HOOK", "PROBLEM", "SETUP", "DEMO", "PROCESS",
    "RESULT", "BEFORE", "AFTER", "APPLY", "CTA",
}
_PREFIX = re.compile(r"^\s*\d{1,2}\s*[-_.:]?\s*", re.IGNORECASE)

def leaked_role_labels(texts: Iterable[str]) -> list[str]:
    leaks = []
    for raw in texts:
        text = _PREFIX.sub("", str(raw or "")).strip().upper()
        if text in FORBIDDEN_ROLE_LABELS:
            leaks.append(str(raw))
    return leaks

def validate_viewer_copy(texts: Iterable[str]) -> bool:
    leaks = leaked_role_labels(texts)
    if leaks:
        raise ValueError(f"internal role labels leaked into viewer copy: {leaks}")
    return True

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "viewer_facing_copy_only": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
