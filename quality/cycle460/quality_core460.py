"""Reusable proof-first short-video contract for ten genres (review-only)."""
from __future__ import annotations

def validate_beats(beats, *, total=20, hook_limit=1.5):
    """Reject missing, overlapping, late-hook or blank-caption beats."""
    if not beats or beats[0].start != 0 or beats[-1].end != total:
        raise ValueError('incomplete timeline')
    if beats[0].end > hook_limit:
        raise ValueError('hook too late')
    for i, beat in enumerate(beats):
        if beat.start >= beat.end or not beat.caption.strip():
            raise ValueError('invalid beat')
        if i and beats[i-1].end != beat.start:
            raise ValueError('gap or overlap')
    return True

def validate_evidence(rows, ids, claimed_sum):
    """Verify on-screen proof IDs against synthetic rows, not an invented result."""
    if not rows or len(set(r[0] for r in rows)) != len(rows):
        raise ValueError('invalid rows')
    actual = [r for r in rows if r[0] in ids]
    if len(actual) != len(ids) or sum(r[2] for r in actual) != claimed_sum:
        raise ValueError('unproven result')
    return True

def publication_gate(manifest):
    if manifest.get('rights') != 'SYNTHETIC_ORIGINAL':
        raise ValueError('rights unverified')
    if manifest.get('auto_post') is not False or manifest.get('publication') != 'NOT_APPROVED':
        raise ValueError('publication forbidden')
    if not manifest.get('japanese_narration_verified'):
        return 'REVIEW_ONLY_NO_JAPANESE_VOICE'
    if not manifest.get('caption_voice_sync_verified'):
        return 'REVIEW_ONLY_NO_SYNC'
    return 'HUMAN_REVIEW_REQUIRED'
