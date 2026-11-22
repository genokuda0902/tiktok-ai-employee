"""Fail-closed review metadata validation; not proof of Japanese speech."""
def review_gate(meta):
    issues = []
    if meta.get("width", 0) < 1080 or meta.get("height", 0) < 1920:
        issues.append("resolution_below_target")
    if meta.get("fps", 0) < 24:
        issues.append("fps_below_target")
    if not meta.get("caption_safe_area_checked", False):
        issues.append("caption_safe_area_unverified")
    if not meta.get("japanese_narration_verified", False):
        issues.append("japanese_narration_unverified")
    if not meta.get("speech_caption_sync_verified", False):
        issues.append("speech_caption_sync_unverified")
    if not meta.get("assets_approved", False):
        issues.append("assets_unapproved")
    if not meta.get("employee_approved", False):
        issues.append("employee_approval_missing")
    return {"publication_approved": not issues, "issues": issues}
