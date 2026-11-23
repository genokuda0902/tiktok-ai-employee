"""Fail-closed review gate for Japanese narration (cycle1652)."""
import json
import subprocess

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=[s for s in streams if s.get("codec_type")=="audio"]
    return {"video_present":video is not None,"width":video.get("width") if video else None,"height":video.get("height") if video else None,"audio_present":bool(audio),"japanese_speech_verified":False,"caption_sync_verified":False,"posting_allowed":False,"quality_approved":False}

def can_post(report):
    return all(report.get(k) is True for k in ("video_present","audio_present","japanese_speech_verified","caption_sync_verified","quality_approved")) and report.get("posting_allowed") is True
