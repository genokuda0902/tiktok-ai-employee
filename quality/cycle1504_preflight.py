"""Fail-closed review gate: AAC audio is not proof of Japanese narration."""
import json
import subprocess

def inspect(path, narration_verified=False, captions_verified=False, human_approved=False):
    probe = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(probe.stdout)
    streams=data["streams"]
    video=next((s for s in streams if s["codec_type"]=="video"),None)
    audio=next((s for s in streams if s["codec_type"]=="audio"),None)
    issues=[]
    if not video or video.get("width",0)<720 or video.get("height",0)<1280: issues.append("video_resolution")
    if not audio: issues.append("audio_missing")
    if not narration_verified: issues.append("japanese_narration_unverified")
    if not captions_verified: issues.append("caption_sync_unverified")
    if not human_approved: issues.append("human_approval_missing")
    return {"publication_approved":not issues,"issues":issues}
