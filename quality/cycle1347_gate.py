"""Fail-closed technical gate for review-only MP4s (not a publication approval)."""
import json
import subprocess
from pathlib import Path

def inspect_mp4(path, *, narration_verified=False, captions_verified=False, rights_approved=False, human_approved=False):
    p=Path(path)
    if not p.is_file():
        return {"passed":False,"issues":["missing_file"]}
    try:
        data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)],timeout=20))
    except (subprocess.SubprocessError,ValueError,OSError):
        return {"passed":False,"issues":["probe_failed"]}
    videos=[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]
    audios=[s for s in data.get("streams",[]) if s.get("codec_type")=="audio"]
    issues=[]
    if not videos: issues.append("missing_video")
    elif (videos[0].get("width"),videos[0].get("height"))!=(1080,1920): issues.append("wrong_resolution")
    if not audios: issues.append("missing_audio")
    if not narration_verified: issues.append("japanese_narration_unverified")
    if not captions_verified: issues.append("caption_sync_unverified")
    if not rights_approved: issues.append("asset_rights_unapproved")
    if not human_approved: issues.append("human_approval_missing")
    return {"passed":not issues,"issues":issues,"resolution":([videos[0].get("width"),videos[0].get("height")] if videos else None),"audio_streams":len(audios)}
