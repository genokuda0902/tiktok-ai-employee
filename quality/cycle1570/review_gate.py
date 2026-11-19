"""Fail-closed review checks for 10-category video prototypes."""

def review_gate(metadata):
    reasons=[]
    if metadata.get("width",0)<720 or metadata.get("height",0)<1280:
        reasons.append("vertical_resolution")
    if not metadata.get("japanese_speech_verified",False):
        reasons.append("japanese_speech_unverified")
    if not metadata.get("captions_synced_verified",False):
        reasons.append("caption_sync_unverified")
    if not metadata.get("assets_approved",False):
        reasons.append("assets_not_approved")
    if not metadata.get("employee_approved",False):
        reasons.append("employee_not_approved")
    return {"approved":not reasons,"reasons":reasons}
