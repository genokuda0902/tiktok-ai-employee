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
    result_beats = [b for b in beats if isinstance(b, dict) and str(b.get("phase","")).upper()=="RESULT"]
    if result_beats and not any(bool(b.get("comparison")) for b in result_beats):
        errors.append("result_comparison_missing")
    # If timing metadata is supplied, require enough uninterrupted RESULT dwell to read proof.
    timed_results = [b for b in result_beats if "duration_s" in b]
    if timed_results:
        try:
            max_result_dwell = max(float(b.get("duration_s", 0)) for b in timed_results)
        except (TypeError, ValueError):
            errors.append("result_duration_invalid")
        else:
            if max_result_dwell < 2.0:
                errors.append("result_dwell_too_short")
    if any(bool(b.get("auto_post")) for b in beats if isinstance(b, dict)):
        errors.append("auto_post_forbidden")
    if any(str(b.get("publication","")).upper() == "APPROVED" for b in beats if isinstance(b, dict)):
        errors.append("publication_must_require_human_review")
    return not errors, errors
