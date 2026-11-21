"""Fail-closed media probe for review-only synthetic TikTok drafts."""
import json
import subprocess

def inspect(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    return {"width":video.get("width") if video else None,"height":video.get("height") if video else None,"duration":float(data.get("format",{}).get("duration",0)),"audio_track":audio is not None}

def publication_gate(metadata):
    required=("rights_approved","privacy_approved","japanese_narration_verified","captions_synced_verified","human_approved")
    return all(metadata.get(k) is True for k in required) and metadata.get("audio_track") is True and metadata.get("width",0)>=720 and metadata.get("height",0)>=1280
