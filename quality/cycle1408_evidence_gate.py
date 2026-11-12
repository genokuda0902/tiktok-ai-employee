"""Fail-closed review evidence gate; never equate AAC presence with speech."""
def evaluate(meta):
    reasons=[]
    if meta.get("width") != 1080 or meta.get("height") != 1920:
        reasons.append("portrait_resolution")
    if not meta.get("full_decode_pass"):
        reasons.append("decode")
    if not meta.get("japanese_speech_verified"):
        reasons.append("japanese_speech_unverified")
    if not meta.get("speech_caption_sync_verified"):
        reasons.append("caption_sync_unverified")
    if not meta.get("asset_rights_approved"):
        reasons.append("asset_rights_unapproved")
    if not meta.get("employee_approved"):
        reasons.append("employee_unapproved")
    return {"publication_approved":not reasons,"reasons":reasons}
