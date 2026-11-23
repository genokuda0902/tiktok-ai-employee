"""Fail-closed cross-genre vertical video QA (cycle1665)."""
def check_manifest(manifest):
    problems = []
    if manifest.get("width") != 1080 or manifest.get("height") != 1920:
        problems.append("vertical_resolution")
    if not manifest.get("japanese_narration_verified"):
        problems.append("narration_missing")
    if not manifest.get("speech_caption_sync_verified"):
        problems.append("caption_sync_missing")
    if not manifest.get("assets_approved"):
        problems.append("assets_unapproved")
    if not manifest.get("employee_approved"):
        problems.append("employee_approval_missing")
    for caption in manifest.get("captions", []):
        if caption.get("bottom_y", 1920) > 1600:
            problems.append("caption_outside_safe_zone")
    return sorted(set(problems))
