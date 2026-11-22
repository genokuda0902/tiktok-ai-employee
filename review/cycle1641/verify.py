#!/usr/bin/env python3
"""Fail-closed media verification: stream presence is not speech validation."""
import json
import subprocess
import sys

def inspect(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    video = [s for s in data["streams"] if s["codec_type"] == "video"]
    audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
    assert len(video) == 1 and video[0]["width"] == 1080 and video[0]["height"] == 1920
    assert video[0]["codec_name"] == "h264"
    assert 19.8 <= float(data["format"]["duration"]) <= 20.2
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"], check=True)
    return {"video_ok": True, "audio_stream": bool(audio), "japanese_narration_verified": False, "speech_caption_sync_verified": False, "publication_approved": False}

if __name__ == "__main__":
    report = inspect(sys.argv[1])
    print(json.dumps(report, ensure_ascii=False))
    if not report["japanese_narration_verified"]:
        print("REVIEW ONLY: Japanese narration missing/unverified", file=sys.stderr)
