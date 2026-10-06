"""Fail-closed gate for Japanese narration evidence.

Validation only. This module never publishes or posts media.
"""

def validate_japanese_narration(evidence):
    errors = []
    if not isinstance(evidence, dict):
        return False, ["narration_evidence_missing"]

    if str(evidence.get("language", "")).lower() not in {"ja", "ja-jp"}:
        errors.append("japanese_language_unverified")
    if not str(evidence.get("audio_path", "")).strip():
        errors.append("narration_audio_missing")
    try:
        duration = float(evidence.get("duration_seconds"))
    except (TypeError, ValueError):
        duration = 0.0
    if duration <= 0:
        errors.append("narration_duration_invalid")
    if not bool(evidence.get("semantic_sync_verified")):
        errors.append("narration_semantic_sync_unverified")
    if not bool(evidence.get("human_review_required", True)):
        errors.append("human_review_must_be_required")
    if bool(evidence.get("auto_post")):
        errors.append("auto_post_forbidden")
    if str(evidence.get("publication", "")).upper() == "APPROVED":
        errors.append("publication_must_require_human_review")
    return not errors, errors
