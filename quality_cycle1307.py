"""Review-only video QA. Does not certify publication readiness."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def validate(path, narration_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    data=probe(path)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=any(s.get("codec_type")=="audio" for s in streams)
    decoded=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True).returncode==0
    return {"video_decodes":decoded,"resolution":[video.get("width"),video.get("height")],"duration":float(data["format"]["duration"]),"audio_stream":audio,"japanese_narration_verified":bool(narration_verified and audio),"captions_synced":bool(captions_synced),"assets_approved":bool(assets_approved),"employee_approved":bool(employee_approved),"posting_allowed":bool(decoded and video.get("width",0)>=1080 and video.get("height",0)>=1920 and audio and narration_verified and captions_synced and assets_approved and employee_approved)}
