"""Fail-closed media gate shared by all content genres."""
def inspect_streams(probe, *, japanese_voice_verified=False, captions_synced=False, rights_approved=False, employee_approved=False):
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    problems = []
    if not video or video.get("width") != 1080 or video.get("height") != 1920:
        problems.append("video_format")
    if not audio: problems.append("audio_missing")
    if not japanese_voice_verified: problems.append("japanese_voice_unverified")
    if not captions_synced: problems.append("captions_unsynced")
    if not rights_approved: problems.append("rights_unapproved")
    if not employee_approved: problems.append("employee_unapproved")
    return {"publication_approved": not problems, "problems": problems}
