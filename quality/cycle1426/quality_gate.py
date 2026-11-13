"""Reusable fail-closed media quality checks for all ten genres."""
def review_status(video_stream, audio_stream, narration_verified=False, captions_synced=False, rights_approved=False, employee_approved=False):
    issues=[]
    if video_stream.get("codec_name") != "h264" or (video_stream.get("width"), video_stream.get("height")) != (1080,1920):
        issues.append("invalid_video")
    if audio_stream.get("codec_name") != "aac":
        issues.append("missing_aac_audio")
    if not narration_verified: issues.append("japanese_narration_unverified")
    if not captions_synced: issues.append("speech_caption_sync_unverified")
    if not rights_approved: issues.append("rights_unapproved")
    if not employee_approved: issues.append("employee_unapproved")
    return {"publication_approved": not issues, "issues":issues}
