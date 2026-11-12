"""Reusable QA gate for synthetic animated spreadsheet review videos.
Never infer spoken Japanese from a present AAC stream.
"""
def assess(meta):
    errors=[]
    video=next((s for s in meta.get("streams",[]) if s.get("codec_type")=="video"),None)
    if not video or video.get("width")!=1080 or video.get("height")!=1920: errors.append("resolution")
    if not meta.get("full_decode"): errors.append("decode")
    if not meta.get("japanese_narration_verified"): errors.append("narration")
    if not meta.get("speech_synced_captions_verified"): errors.append("speech_sync")
    if not meta.get("asset_rights_approved"): errors.append("rights")
    if not meta.get("employee_approved"): errors.append("employee")
    return {"posting_allowed":not errors,"issues":errors}
