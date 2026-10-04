"""Fail-closed validation for first-1.5s visual/audio/caption semantic sync."""

HOOK_MAX_SECONDS = 1.5

def validate_hook_semantic_sync(hook):
    if not isinstance(hook, dict):
        return False, ["hook_missing"]
    errors = []
    try:
        start = float(hook.get("start_seconds", 0.0))
        end = float(hook.get("end_seconds"))
    except (TypeError, ValueError):
        return False, ["hook_timing_invalid"]
    if start < 0 or end <= start or end > HOOK_MAX_SECONDS:
        errors.append("hook_outside_first_1_5s")
    claim = str(hook.get("claim_id", "")).strip()
    if not claim:
        errors.append("hook_claim_missing")
    for channel in ("visual_claim_id", "audio_claim_id", "caption_claim_id"):
        value = str(hook.get(channel, "")).strip()
        if not value:
            errors.append(channel + "_missing")
        elif claim and value != claim:
            errors.append(channel + "_mismatch")
    if not str(hook.get("caption_text", "")).strip():
        errors.append("hook_caption_missing")
    if not str(hook.get("narration_text", "")).strip():
        errors.append("hook_narration_missing")
    if bool(hook.get("auto_post")):
        errors.append("auto_post_forbidden")
    if str(hook.get("publication", "")).upper() == "APPROVED":
        errors.append("publication_must_require_human_review")
    return not errors, errors
