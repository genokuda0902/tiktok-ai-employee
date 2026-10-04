"""Reusable fail-closed proof-density validation for short-form videos."""

REQUIRED_ORDER = ("INPUT", "TRANSFORM", "RESULT")

def validate_proof_sequence(beats):
    """Validate a genre-independent input -> transform -> result proof sequence."""
    if not isinstance(beats, list) or not beats:
        return False, ["beats_missing"]
    phases = [str(b.get("phase", "")).upper() for b in beats if isinstance(b, dict)]
    errors = []
    positions = []
    for phase in REQUIRED_ORDER:
        try:
            positions.append(phases.index(phase))
        except ValueError:
            errors.append(f"missing_{phase.lower()}")
    if not errors and positions != sorted(positions):
        errors.append("proof_order_invalid")

    input_beats = [b for b in beats if isinstance(b, dict) and str(b.get("phase","")).upper()=="INPUT"]
    result_beats = [b for b in beats if isinstance(b, dict) and str(b.get("phase","")).upper()=="RESULT"]
    if result_beats and not any(bool(b.get("comparison")) for b in result_beats):
        errors.append("result_comparison_missing")

    # When a demo declares an object identity, require the same object to survive
    # INPUT -> RESULT. This prevents a visually impressive but semantically unrelated
    # "after" screen from passing as proof. Omit object_id only for generic sequences.
    input_ids = {str(b.get("object_id")) for b in input_beats if b.get("object_id") not in (None, "")}
    result_ids = {str(b.get("object_id")) for b in result_beats if b.get("object_id") not in (None, "")}
    if input_ids or result_ids:
        if not input_ids or not result_ids or input_ids.isdisjoint(result_ids):
            errors.append("input_result_identity_mismatch")

    if any(bool(b.get("auto_post")) for b in beats if isinstance(b, dict)):
        errors.append("auto_post_forbidden")
    if any(str(b.get("publication","")).upper() == "APPROVED" for b in beats if isinstance(b, dict)):
        errors.append("publication_must_require_human_review")
    return not errors, errors
