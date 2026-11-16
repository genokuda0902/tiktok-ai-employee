"""Review-only reusable video QA. Never equate decodable MP4 with approved Japanese narration."""
import json, subprocess

def inspect(path):
    raw=subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)])
    data=json.loads(raw)
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),{})
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    return {"width":video.get("width"),"height":video.get("height"),"audio_track":audio is not None,"duration":float(data.get("format",{}).get("duration",0))}

def publication_gate(probe, japanese_narration_verified=False, captions_synced=False, rights_approved=False, employee_approved=False):
    return bool(probe.get("width")==1080 and probe.get("height")==1920 and probe.get("audio_track") and japanese_narration_verified and captions_synced and rights_approved and employee_approved)
