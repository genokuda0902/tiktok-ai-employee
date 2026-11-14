"""Fail-closed media QA. No track alone proves Japanese narration."""
def assess(video_width, video_height, decode_ok, audio_stream, japanese_speech_verified, captions_synced, asset_approved, human_approved):
    problems=[]
    if (video_width,video_height)!=(1080,1920): problems.append("resolution")
    if not decode_ok: problems.append("decode")
    if not audio_stream or not japanese_speech_verified: problems.append("japanese_narration")
    if not captions_synced: problems.append("caption_sync")
    if not asset_approved: problems.append("asset_rights")
    if not human_approved: problems.append("human_approval")
    return {"posting_allowed":not problems,"issues":problems}
