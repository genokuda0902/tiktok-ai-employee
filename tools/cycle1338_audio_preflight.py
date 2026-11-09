"""Fail closed when a review MP4 has no narration or is below vertical HD."""
import json
import subprocess
from pathlib import Path

def check(path):
    p = Path(path)
    if not p.is_file() or not p.stat().st_size:
        return {"approved": False, "errors": ["missing_media"]}
    try:
        raw = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(p)], check=True, capture_output=True, text=True)
        streams = json.loads(raw.stdout).get("streams", [])
    except (OSError, ValueError, subprocess.CalledProcessError):
        return {"approved": False, "errors": ["probe_failed"]}
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    errors = []
    if video is None:
        errors.append("missing_video")
    elif int(video.get("width", 0)) < 1080 or int(video.get("height", 0)) < 1920:
        errors.append("low_resolution")
    if audio is None:
        errors.append("missing_audio")
    if video:
        try:
            subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(p), "-f", "null", "-"], check=True, capture_output=True)
        except (OSError, subprocess.CalledProcessError):
            errors.append("decode_failed")
    return {"approved": not errors, "errors": errors}

if __name__ == "__main__":
    import sys
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["approved"] else 2)
