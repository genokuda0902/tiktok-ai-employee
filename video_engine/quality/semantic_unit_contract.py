"""Reusable fail-closed semantic-unit contract for visual/audio/caption sync.

Validation only. No publishing or external delivery.
"""

def validate_semantic_units(units):
    if not isinstance(units, list) or not units:
        return False, ["semantic_units_missing"]
    errors = []
    previous_end = None
    for i, unit in enumerate(units):
        if not isinstance(unit, dict):
            errors.append(f"unit_{i}_invalid")
            continue
        claim = str(unit.get("claim_id", "")).strip()
        if not claim:
            errors.append(f"unit_{i}_claim_missing")
        try:
            start = float(unit.get("start_seconds"))
            end = float(unit.get("end_seconds"))
        except (TypeError, ValueError):
            errors.append(f"unit_{i}_timing_invalid")
            continue
        if start < 0 or end <= start:
            errors.append(f"unit_{i}_timing_invalid")
        if previous_end is not None and start < previous_end:
            errors.append(f"unit_{i}_overlaps_previous")
        previous_end = max(previous_end or 0, end)
        for channel in ("visual_claim_id", "audio_claim_id", "caption_claim_id"):
            value = str(unit.get(channel, "")).strip()
            if not value:
                errors.append(f"unit_{i}_{channel}_missing")
            elif claim and value != claim:
                errors.append(f"unit_{i}_{channel}_mismatch")
        if not str(unit.get("narration_text", "")).strip():
            errors.append(f"unit_{i}_narration_missing")
        if not str(unit.get("caption_text", "")).strip():
            errors.append(f"unit_{i}_caption_missing")
        if bool(unit.get("auto_post")):
            errors.append("auto_post_forbidden")
        if str(unit.get("publication", "")).upper() == "APPROVED":
            errors.append("publication_must_require_human_review")
    return not errors, errors
