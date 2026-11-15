"""Cycle 1483: fail-closed QA for synthetic review videos. Python stdlib only."""
import json
import subprocess
import sys
from pathlib import Path

def inspect(path):
    data = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)], text=True))
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    return {
        "video_present": video is not None,
        "resolution": [video.get("width"), video.get("height")] if video else None,
        "audio_present": bool(audio),
        "japanese_narration_verified": False,
        "caption_sync_verified": False,
        "rights_verified": False,
        "human_approved": False,
        "posting_allowed": False,
        "status": "PUBLICATION_NOT_APPROVED",
    }

def main():
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
