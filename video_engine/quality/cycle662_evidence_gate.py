"""Generic result-before-claim gate for review-only short-form video scenes.

A claim must not be visible before the corresponding recorded evidence appears.
This module never uploads, posts, merges, or approves media.
"""
from __future__ import annotations

def first_stable_evidence(matches: list[bool], consecutive: int = 3) -> int:
    """Return first index with N consecutive verified frames; fail closed."""
    if consecutive < 2:
        raise ValueError("require stable evidence")
    for index in range(len(matches) - consecutive + 1):
        if all(matches[index:index + consecutive]):
            return index
    raise ValueError("no stable evidence")

def claim_visible(frame_index: int, onset_index: int, evidence_verified: bool) -> bool:
    """Never reveal a numeric/result claim before its verified visual frame."""
    return evidence_verified and frame_index >= onset_index

def release_allowed(*, narration_verified: bool, rights_approved: bool,
                    human_approved: bool, subtitle_sync_verified: bool) -> bool:
    """Technical success alone never grants permission to publish."""
    return all((narration_verified, rights_approved, human_approved,
                subtitle_sync_verified))
