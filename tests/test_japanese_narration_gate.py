"""Cycle 371: fail-closed Japanese narration quality gate.

Reusable across all content genres. This does not synthesize speech; it prevents
publication approval when Japanese narration has not been verified.
"""

def narration_gate(*, language, narration_present, semantic_sync_verified,
                   human_review_required=True, publication_approved=False):
    reasons = []
    if language != "ja":
        reasons.append("language_not_ja")
    if not narration_present:
        reasons.append("narration_missing")
    if not semantic_sync_verified:
        reasons.append("semantic_sync_unverified")
    if not human_review_required:
        reasons.append("human_review_must_remain_required")
    if publication_approved:
        reasons.append("publication_must_remain_unapproved")
    return {"ok": not reasons, "reasons": reasons}


def test_passes_only_verified_japanese_narration():
    r = narration_gate(language="ja", narration_present=True,
                       semantic_sync_verified=True)
    assert r["ok"] is True


def test_fails_non_japanese_or_missing_narration():
    assert "language_not_ja" in narration_gate(
        language="en", narration_present=True, semantic_sync_verified=True
    )["reasons"]
    assert "narration_missing" in narration_gate(
        language="ja", narration_present=False, semantic_sync_verified=True
    )["reasons"]


def test_fails_unverified_semantic_sync():
    assert "semantic_sync_unverified" in narration_gate(
        language="ja", narration_present=True, semantic_sync_verified=False
    )["reasons"]


def test_never_auto_approves_publication():
    assert "publication_must_remain_unapproved" in narration_gate(
        language="ja", narration_present=True, semantic_sync_verified=True,
        publication_approved=True
    )["reasons"]
