"""Review-only QA contract: never approve silent videos or absent human signoff."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe","-v","error","-show_streams","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)["streams"]

def evaluate(streams, *, captions_synced=False, assets_approved=False, employee_approved=False):
    video = next((s for s in streams if s.get("codec_type")=="video"), None)
    audio = next((s for s in streams if s.get("codec_type")=="audio"), None)
    issues=[]
    if not video or video.get("width",0)<1080 or video.get("height",0)<1920: issues.append("resolution")
    if not audio: issues.append("audio_missing")
    if not captions_synced: issues.append("captions_unverified")
    if not assets_approved: issues.append("assets_unapproved")
    if not employee_approved: issues.append("employee_unapproved")
    return {"publication_approved":not issues,"issues":issues}
