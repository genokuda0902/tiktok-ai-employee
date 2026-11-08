"""Fail-closed review-only MP4 checks, reusable across 10 genres."""
import json
import subprocess
from pathlib import Path

def inspect_video(path, *, narration_verified=False, captions_verified=False,
                  assets_approved=False, employee_approved=False):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,width,height,codec_name:format=duration",
         "-of", "json", str(path)], capture_output=True, text=True, check=True)
    meta = json.loads(probe.stdout)
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = any(s.get("codec_type") == "audio" for s in streams)
    checks = {
        "vertical_1080p": video.get("width", 0) >= 1080 and video.get("height", 0) >= 1920,
        "has_audio_stream": audio,
        "japanese_narration_verified": bool(audio and narration_verified),
        "timed_captions_verified": bool(captions_verified),
        "assets_approved": bool(assets_approved),
        "employee_approved": bool(employee_approved),
    }
    return {"checks": checks, "publish_allowed": all(checks.values()),
            "duration": float(meta.get("format", {}).get("duration", 0))}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect_video(Path(sys.argv[1])), ensure_ascii=False, indent=2))
