"""Fail-closed checks for review-only TikTok clips (all genres)."""
def review_gate(probe, *, narration_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    streams=probe.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video"), None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"), None)
    issues=[]
    if not video or video.get("width")!=1080 or video.get("height")!=1920:
        issues.append("vertical_1080p_missing")
    if not audio or not narration_verified:
        issues.append("japanese_narration_unverified")
    if not captions_synced:
        issues.append("caption_sync_unverified")
    if not assets_approved:
        issues.append("assets_not_approved")
    if not employee_approved:
        issues.append("employee_approval_missing")
    return {"approved_for_manual_post":not issues, "issues":issues}
