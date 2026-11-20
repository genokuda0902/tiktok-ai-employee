"""Shared publication gate. No automatic publication."""
def check_video(probe, *, japanese_voice_verified=False, caption_sync_verified=False, asset_approved=False, employee_approved=False):
    streams=probe.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    issues=[]
    if not video or video.get("width",0)<720 or video.get("height",0)<1280: issues.append("video_resolution")
    if not audio: issues.append("missing_audio")
    if not japanese_voice_verified: issues.append("japanese_voice_unverified")
    if not caption_sync_verified: issues.append("caption_sync_unverified")
    if not asset_approved: issues.append("asset_approval_missing")
    if not employee_approved: issues.append("employee_approval_missing")
    return {"approved":not issues,"issues":issues}
