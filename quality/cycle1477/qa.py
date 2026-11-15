"""Fail-closed QA for review-only TikTok MP4. Stdlib + ffprobe/ffmpeg only."""
import json
import subprocess
import sys
from pathlib import Path

def check(path):
    path = Path(path)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    meta = json.loads(probe.stdout)
    videos = [s for s in meta["streams"] if s["codec_type"] == "video"]
    audios = [s for s in meta["streams"] if s["codec_type"] == "audio"]
    if len(videos) != 1:
        raise ValueError("Exactly one video stream required")
    video = videos[0]
    if video["width"] * 16 != video["height"] * 9:
        raise ValueError("Vertical 9:16 required")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], check=True)
    return {
        "width": video["width"], "height": video["height"],
        "duration": float(meta["format"]["duration"]),
        "audio_stream_present": bool(audios),
        "japanese_narration_verified": False,
        "speech_caption_sync_verified": False,
        "rights_approved": False,
        "human_approved": False,
        "posting_allowed": False,
        "status": "PUBLICATION_NOT_APPROVED",
    }

if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1]), ensure_ascii=False, indent=2))
