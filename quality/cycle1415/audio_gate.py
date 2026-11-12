"""Fail-closed review gate for generated MP4 metadata; genre independent."""
def assess(probe, *, narration_verified=False, captions_synced=False,
           asset_rights_approved=False, employee_approved=False):
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    reasons = []
    if video.get("codec_name") != "h264" or video.get("width") != 1080 or video.get("height") != 1920:
        reasons.append("video_spec_unverified")
    if not audio:
        reasons.append("audio_stream_missing")
    if not narration_verified:
        reasons.append("japanese_narration_unverified")
    if not captions_synced:
        reasons.append("caption_sync_unverified")
    if not asset_rights_approved:
        reasons.append("asset_rights_unapproved")
    if not employee_approved:
        reasons.append("employee_approval_missing")
    return {"posting_allowed": not reasons, "status": "APPROVED" if not reasons else "REVIEW_ONLY", "reasons": reasons}
