"""Fail-closed media stream gate for review-only TikTok MP4s (stdlib)."""
import json
import subprocess
import sys
from pathlib import Path

def inspect(path):
    data = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)], text=True))
    streams = data.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    v = videos[0] if videos else {}
    return {
        "video": bool(videos),
        "audio": bool(audios),
        "width": v.get("width", 0),
        "height": v.get("height", 0),
        "duration": float(data.get("format", {}).get("duration", 0)),
        "publication_allowed": False,
        "reasons": (["missing_audio"] if not audios else [])
                   + (["resolution_below_1080x1920"] if v.get("width", 0) < 1080 or v.get("height", 0) < 1920 else [])
                   + ["human_asset_and_caption_approval_required"],
    }

if __name__ == "__main__":
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))
