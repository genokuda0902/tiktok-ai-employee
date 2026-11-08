"""Fail-closed review gate shared by all ten genres."""
def review(meta):
    failures=[]
    if meta.get("width")!=1080 or meta.get("height")!=1920: failures.append("resolution")
    if not meta.get("video_decodes"): failures.append("decode")
    if not meta.get("japanese_narration_verified"): failures.append("narration")
    if not meta.get("captions_speech_aligned"): failures.append("caption_sync")
    if not meta.get("assets_rights_approved"): failures.append("rights")
    if not meta.get("privacy_checked"): failures.append("privacy")
    if not meta.get("employee_approved"): failures.append("employee_approval")
    return {"approved":not failures,"failures":failures}
