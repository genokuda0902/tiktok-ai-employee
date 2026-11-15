"""Fail-closed review gate for reusable 10-genre MP4 renders (stdlib only)."""
import json
import subprocess
from pathlib import Path

def inspect(video: str, srt: str, approved: bool = False) -> dict:
    video_path, subtitle_path = Path(video), Path(srt)
    if not video_path.is_file():
        raise FileNotFoundError(video)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video_path)],
        capture_output=True, text=True, check=True)
    data = json.loads(probe.stdout)
    streams = data.get("streams", [])
    pictures = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    vertical = bool(pictures and pictures[0].get("width", 0) < pictures[0].get("height", 0))
    subtitles = subtitle_path.is_file() and "-->" in subtitle_path.read_text(encoding="utf-8")
    # Audio codec existence is not evidence of Japanese narration or synchronization.
    return {
        "vertical": vertical,
        "audio_stream_present": bool(audio),
        "japanese_narration_verified": False,
        "captions_present": bool(subtitles),
        "caption_audio_sync_verified": False,
        "human_approved": bool(approved),
        "posting_allowed": False,
        "quality_status": "REVIEW_ONLY",
    }
