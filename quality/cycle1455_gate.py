"""Fail-closed cross-genre review gate. No score can override missing audio or approval."""
def assess(probe, *, rights_approved=False, human_approved=False, captions_verified=False):
    streams=probe.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video"), None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"), None)
    reasons=[]
    if not video or video.get("width")!=1080 or video.get("height")!=1920:
        reasons.append("vertical_1080x1920_missing")
    if not audio: reasons.append("japanese_narration_missing")
    if not captions_verified: reasons.append("synchronized_captions_unverified")
    if not rights_approved: reasons.append("rights_unapproved")
    if not human_approved: reasons.append("human_review_unapproved")
    return {"publication_approved": not reasons, "reasons": reasons}
