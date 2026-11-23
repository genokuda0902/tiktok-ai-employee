"""Fail-closed narration and approval QA shared across all genres."""
import json
import subprocess

def inspect(mp4, evidence):
    streams=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(mp4)],text=True)).get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    reasons=[]
    if not video or (video.get("width"),video.get("height"))!=(1080,1920):
        reasons.append("vertical_video_missing_or_wrong_size")
    if not audio: reasons.append("audio_stream_missing")
    if evidence.get("narration_language")!="ja" or not evidence.get("narration_source_verified"):
        reasons.append("japanese_narration_unverified")
    if not evidence.get("caption_timing_verified"): reasons.append("caption_timing_unverified")
    if not evidence.get("asset_rights_approved"): reasons.append("asset_rights_unapproved")
    if not evidence.get("employee_approved"): reasons.append("employee_approval_missing")
    return {"approved":not reasons,"reasons":reasons}
