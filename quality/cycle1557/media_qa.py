"""Fail-closed review-only MP4 checks, reusable across content genres."""
import json, subprocess
from pathlib import Path

def inspect(path, *, narration_verified=False, caption_sync_verified=False, rights_approved=False, employee_approved=False):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data["streams"]
    video=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    fps=video.get("r_frame_rate","0/1")
    n,d=map(int,fps.split("/"))
    result={"resolution":[video.get("width"),video.get("height")],"fps":n/d if d else 0,"duration":float(data["format"].get("duration",0)),"audio_track":bool(audio),"narration_verified":narration_verified,"caption_sync_verified":caption_sync_verified,"rights_approved":rights_approved,"employee_approved":employee_approved}
    result["publication_approved"]=all((result["resolution"]==[1080,1920],result["fps"]>=24,result["audio_track"],narration_verified,caption_sync_verified,rights_approved,employee_approved))
    return result
