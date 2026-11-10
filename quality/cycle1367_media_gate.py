"""Offline media QA: AAC presence is not proof of Japanese narration."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(result.stdout)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=next((s for s in streams if s.get("codec_type")=="audio"),{})
    return {"width":video.get("width"),"height":video.get("height"),"video_codec":video.get("codec_name"),"audio_codec":audio.get("codec_name"),"duration":float(data.get("format",{}).get("duration",0))}

def publication_gate(measured, *, japanese_narration_verified=False, synchronized_captions_verified=False, rights_approved=False, employee_approved=False):
    reasons=[]
    if measured.get("video_codec")!="h264" or (measured.get("width"),measured.get("height")) not in ((720,1280),(1080,1920)): reasons.append("video_format")
    if not measured.get("audio_codec"): reasons.append("audio_missing")
    if not japanese_narration_verified: reasons.append("japanese_narration_unverified")
    if not synchronized_captions_verified: reasons.append("caption_sync_unverified")
    if not rights_approved: reasons.append("rights_unapproved")
    if not employee_approved: reasons.append("employee_unapproved")
    return {"approved":not reasons,"reasons":reasons}
