"""Fail-closed QA: an AAC stream or sound effect is not Japanese narration."""
def assess(video_streams, japanese_speech_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    video=any(s.get("codec_type")=="video" for s in video_streams)
    audio=any(s.get("codec_type")=="audio" for s in video_streams)
    reasons=[]
    if not video: reasons.append("video_missing")
    if not audio: reasons.append("audio_missing")
    if not japanese_speech_verified: reasons.append("japanese_narration_unverified")
    if not captions_synced: reasons.append("speech_caption_sync_unverified")
    if not assets_approved: reasons.append("assets_unapproved")
    if not employee_approved: reasons.append("employee_approval_missing")
    return {"publication_approved":not reasons,"reasons":reasons}
