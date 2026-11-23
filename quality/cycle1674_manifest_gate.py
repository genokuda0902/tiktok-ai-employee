"""Fail-closed media manifest validation, reusable across all ten genres."""
def validate(manifest):
    errors = []
    if manifest.get("publication_approved") is not True:
        errors.append("publication approval missing")
    if manifest.get("asset_rights_approved") is not True:
        errors.append("asset rights unapproved")
    if manifest.get("privacy_checked") is not True:
        errors.append("privacy not checked")
    if manifest.get("japanese_narration_verified") is not True:
        errors.append("Japanese narration unverified")
    if manifest.get("captions_synced") is not True:
        errors.append("captions unsynchronized")
    if manifest.get("video_decode_passed") is not True:
        errors.append("video decode unverified")
    if manifest.get("width", 0) < 720 or manifest.get("height", 0) < 1280:
        errors.append("insufficient resolution")
    return {"posting_allowed": not errors, "errors": errors}
