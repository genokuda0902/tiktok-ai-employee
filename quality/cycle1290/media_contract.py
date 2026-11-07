"""Reusable review-only media contract; fail closed on missing audio."""
import json
import subprocess

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height","-show_entries","format=duration","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=any(s.get("codec_type")=="audio" for s in streams)
    return {"video":bool(video),"vertical_1080p":bool(video and video.get("width")==1080 and video.get("height")==1920),"audio":audio,"duration":float(data.get("format",{}).get("duration",0))}

def publication_allowed(media, approved_assets=False, approved_staff=False, synced_captions=False):
    return bool(media["video"] and media["vertical_1080p"] and media["audio"] and synced_captions and approved_assets and approved_staff)
