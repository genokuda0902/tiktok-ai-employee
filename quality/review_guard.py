"""Cross-genre fail-closed publication gate."""
def validate(media, approved=False):
    errors = []
    if media.get("width", 0) < 720 or media.get("height", 0) < 1280: errors.append("resolution")
    if media.get("video_codec") != "h264": errors.append("codec")
    if not media.get("japanese_narration_verified"): errors.append("narration")
    if not media.get("captions_synchronized"): errors.append("captions")
    if not media.get("rights_cleared"): errors.append("rights")
    if not approved: errors.append("employee_approval")
    return {"publication_allowed": not errors, "errors": errors}
