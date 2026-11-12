"""Fail-closed audio evidence: an AAC stream is not Japanese narration."""
import json
import subprocess

def inspect(path, narration_verified=False, subtitles_verified=False, rights_approved=False, employee_approved=False):
    raw = subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)], text=True)
    data = json.loads(raw)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    resolution_ok = (video.get("width"),video.get("height")) == (1080,1920)
    return {"audio_track_present":has_audio,"japanese_narration_verified":bool(narration_verified),
            "subtitles_verified":bool(subtitles_verified),"resolution_ok":resolution_ok,
            "publication_allowed":all([has_audio,narration_verified,subtitles_verified,
                                       resolution_ok,rights_approved,employee_approved])}
