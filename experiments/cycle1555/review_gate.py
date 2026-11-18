"""Review-only media validation. Presence of AAC does not establish speech."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def review_gate(metadata, *, narration_verified=False, captions_aligned=False, rights_approved=False, employee_approved=False):
    streams = metadata.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    checks = {
        "portrait_720_min": video.get("width", 0) >= 720 and video.get("height", 0) >= 1280,
        "h264": video.get("codec_name") == "h264",
        "audio_track": bool(audio),
        "japanese_narration_verified": narration_verified,
        "captions_aligned": captions_aligned,
        "rights_approved": rights_approved,
        "employee_approved": employee_approved,
    }
    return {"checks": checks, "publishable": all(checks.values())}
