"""Fail-closed checks for review-only video metadata; no silent AAC as narration."""
def validate(meta):
    failures=[]
    if (meta.get("width"),meta.get("height")) != (1080,1920): failures.append("resolution")
    if not meta.get("video_decodes"): failures.append("decode")
    if not meta.get("japanese_narration_verified"): failures.append("narration")
    if not meta.get("captions_synchronized"): failures.append("caption_sync")
    if not meta.get("assets_approved"): failures.append("assets")
    if not meta.get("employee_approved"): failures.append("employee_approval")
    return {"posting_allowed":not failures,"failures":failures}
