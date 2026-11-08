"""Fail-closed media metadata gate. Audio stream != Japanese narration."""
import json
import subprocess

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data["streams"]
    v=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=[s for s in streams if s.get("codec_type")=="audio"]
    return {"width":v.get("width",0),"height":v.get("height",0),"duration":float(data["format"].get("duration",0)),"audio_streams":len(audio)}

def publication_gate(metadata, *, narration_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    failures=[]
    if (metadata["width"],metadata["height"]) != (1080,1920): failures.append("resolution")
    if metadata["duration"] <= 0: failures.append("duration")
    if not metadata["audio_streams"]: failures.append("audio_stream")
    if not narration_verified: failures.append("japanese_narration")
    if not captions_synced: failures.append("caption_sync")
    if not assets_approved: failures.append("asset_approval")
    if not employee_approved: failures.append("employee_approval")
    return failures
