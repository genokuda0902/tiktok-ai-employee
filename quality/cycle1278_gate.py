"""Fail-closed review gate for 10-genre MP4 prototypes (cycle1278)."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height:format=duration","-of","json",str(path)]))
    streams=data["streams"]
    video=next((s for s in streams if s["codec_type"]=="video"),None)
    audio=next((s for s in streams if s["codec_type"]=="audio"),None)
    return {"video": bool(video), "resolution": [video.get("width"),video.get("height")] if video else None, "duration":float(data["format"]["duration"]), "audio":bool(audio), "publish_approved":False}

def publishable(report, approved_assets=False, human_approved=False, synced_captions=False):
    return bool(report["video"] and report["audio"] and report["resolution"]==[1080,1920] and approved_assets and human_approved and synced_captions)
