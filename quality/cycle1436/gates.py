"""Fail-closed review gate for any genre. Synthetic demo is NOT approved."""
def evaluate(meta):
    required = ("public_safe_synthetic", "narration_verified", "subtitle_speech_synced", "employee_approved", "decode_pass", "width", "height")
    missing = [k for k in required if k not in meta]
    blockers = list(missing)
    for key in ("narration_verified", "subtitle_speech_synced", "employee_approved", "decode_pass"):
        if meta.get(key) is not True:
            blockers.append(key)
    if meta.get("width") != 1080 or meta.get("height") != 1920:
        blockers.append("resolution")
    if meta.get("public_safe_synthetic") is not True:
        blockers.append("source_rights")
    return {"posting_allowed": not blockers, "blockers": sorted(set(blockers))}
