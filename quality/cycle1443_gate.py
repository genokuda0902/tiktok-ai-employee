"""Fail-closed technical review for any of the ten genres. No publication approval implied."""
import json
from pathlib import Path

def inspect_probe(probe, *, captions_embedded=False, japanese_voice_verified=False,
                  rights_approved=False, employee_approved=False):
    streams=probe.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video"), {})
    audio=next((s for s in streams if s.get("codec_type")=="audio"), None)
    issues=[]
    if (video.get("width"),video.get("height"))!=(1080,1920):
        issues.append("resolution")
    if video.get("codec_name")!="h264": issues.append("codec")
    if not audio: issues.append("audio_missing")
    if not japanese_voice_verified: issues.append("japanese_voice_unverified")
    if not captions_embedded: issues.append("embedded_captions_unverified")
    if not rights_approved: issues.append("rights_unapproved")
    if not employee_approved: issues.append("employee_unapproved")
    return {"publication_approved":not issues,"issues":issues}

def inspect_file(path, **kwargs):
    import subprocess
    raw=subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(Path(path))])
    return inspect_probe(json.loads(raw),**kwargs)
