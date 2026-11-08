"""Fail-closed video evidence gate; independent of genre and editor."""
import json
import subprocess
from pathlib import Path

def inspect(path, approved_assets=False, employee_approved=False, synced_captions=False):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout)
    streams = data.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    width = int(videos[0].get("width", 0)) if videos else 0
    height = int(videos[0].get("height", 0)) if videos else 0
    duration = float(data.get("format", {}).get("duration", 0))
    checks = {
        "video_present": bool(videos),
        "portrait_1080p": width >= 1080 and height >= 1920 and height > width,
        "duration_15_45s": 15 <= duration <= 45,
        "audio_stream_present": bool(audios),
        "japanese_voice_reviewed": False,  # Never infer language or quality from stream presence
        "captions_sync_reviewed": bool(synced_captions),
        "asset_rights_approved": bool(approved_assets),
        "employee_approved": bool(employee_approved),
    }
    return {"checks": checks, "publication_allowed": all(checks.values()),
            "resolution": [width, height], "duration": duration,
            "status": "PUBLICATION_APPROVED" if all(checks.values()) else "REVIEW_ONLY"}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
