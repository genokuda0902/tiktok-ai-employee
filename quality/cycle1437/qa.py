"""Review-only validation: audio codec does not prove narration."""
def assess(meta):
    failures=[]
    if (meta.get("width"),meta.get("height")) != (1080,1920): failures.append("resolution")
    if not meta.get("full_decode"): failures.append("decode")
    if not meta.get("japanese_speech_verified"): failures.append("narration")
    if not meta.get("speech_caption_sync_verified"): failures.append("sync")
    if not meta.get("rights_approved"): failures.append("rights")
    if not meta.get("employee_approved"): failures.append("approval")
    return {"publication_approved":not failures,"failures":failures}
