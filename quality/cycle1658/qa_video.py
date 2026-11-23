"""Reusable fail-closed QA for 10 genre review MP4s. No publishing."""
import json, subprocess
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))

def evaluate(data, *, japanese_voice_verified=False, captions_verified=False,
             rights_approved=False, employee_approved=False):
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    issues=[]
    if not video or video.get("width")!=1080 or video.get("height")!=1920:
        issues.append("portrait_1080x1920_required")
    if not audio: issues.append("audio_stream_missing")
    if not japanese_voice_verified: issues.append("japanese_speech_unverified")
    if not captions_verified: issues.append("speech_caption_sync_unverified")
    if not rights_approved: issues.append("media_rights_unapproved")
    if not employee_approved: issues.append("employee_approval_missing")
    return {"publication_approved":not issues,"issues":issues}

if __name__=="__main__":
    import sys
    print(json.dumps(evaluate(probe(Path(sys.argv[1]))),ensure_ascii=False,indent=2))
