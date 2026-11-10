"""Fail-closed video quality gate; audio presence alone is not speech verification."""
import json
import subprocess

def inspect_video(path, manifest):
    data = json.loads(subprocess.check_output(
        ["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],
        text=True))
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    issues = []
    if not video or video.get("width") != 1080 or video.get("height") != 1920:
        issues.append("1080x1920 video required")
    if not audio:
        issues.append("audio stream missing")
    for key in ("japanese_narration_verified", "speech_synced_captions_verified",
                "assets_approved", "human_approved"):
        if manifest.get(key) is not True:
            issues.append(key + " not verified")
    return {"publication_allowed": not issues, "issues": issues,
            "duration": float(data.get("format", {}).get("duration", 0))}
