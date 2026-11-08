"""Reusable review-only video gate. Does not certify narration or approval."""
import json, subprocess

def inspect(path):
    raw=subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True)
    meta=json.loads(raw)
    video=next((s for s in meta["streams"] if s["codec_type"]=="video"),None)
    audio=any(s["codec_type"]=="audio" for s in meta["streams"])
    return {"width":video.get("width") if video else None,"height":video.get("height") if video else None,"audio_stream":audio,"duration":float(meta["format"]["duration"])}

def approved(meta, narration_verified=False, captions_synced=False, rights_approved=False, employee_approved=False):
    return bool(meta["width"]>=1080 and meta["height"]>=1920 and meta["audio_stream"] and narration_verified and captions_synced and rights_approved and employee_approved)
