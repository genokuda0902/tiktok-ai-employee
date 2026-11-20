"""Fail-closed media audio evidence. Audio track != Japanese narration."""
import json
import subprocess
from pathlib import Path


def inspect(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(path)
    run = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)], capture_output=True, text=True, check=True)
    meta = json.loads(run.stdout)
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    return {"has_video": bool(video), "width": video.get("width") if video else None, "height": video.get("height") if video else None, "has_audio_track": bool(audio), "japanese_narration_verified": False, "caption_sync_verified": False, "posting_allowed": False, "review_only": True}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
