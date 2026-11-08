"""Fail-closed inspection of review MP4 (stdlib + ffprobe)."""
import json, subprocess, sys
from pathlib import Path

def inspect(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    return {"video_ok":bool(video and video.get("codec_name")=="h264"),"vertical_1080p":bool(video and video.get("width")==1080 and video.get("height")==1920),"duration":float(data["format"]["duration"]),"audio_stream":bool(audio),"narration_verified":False,"caption_sync_verified":False,"publish_approved":False}

def public_ready(evidence):
    return all(evidence.get(k) is True for k in ("video_ok","vertical_1080p","audio_stream","narration_verified","caption_sync_verified","publish_approved"))

if __name__=="__main__":
    print(json.dumps(inspect(Path(sys.argv[1])),ensure_ascii=False,indent=2))
