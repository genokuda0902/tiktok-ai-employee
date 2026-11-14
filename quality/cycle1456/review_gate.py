"""Review-only media QA gate. Reject missing Japanese narration even if an AAC tone exists."""
def assess(video, rights_approved=False, human_approved=False):
    required=("width","height","duration","video_codec","audio_codec","japanese_narration","burned_captions")
    missing=[k for k in required if k not in video]
    reasons=["missing:"+k for k in missing]
    if video.get("width")!=1080 or video.get("height")!=1920: reasons.append("resolution")
    if video.get("video_codec")!="h264": reasons.append("video_codec")
    if video.get("audio_codec")!="aac": reasons.append("audio_codec")
    if not video.get("japanese_narration"): reasons.append("no_japanese_narration")
    if not video.get("burned_captions"): reasons.append("no_burned_captions")
    if not rights_approved: reasons.append("rights_unapproved")
    if not human_approved: reasons.append("human_unapproved")
    return {"publication_approved":not reasons,"reasons":sorted(set(reasons))}
