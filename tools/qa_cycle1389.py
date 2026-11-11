"""Fail-closed QA for review-only vertical MP4; no claim of speech verification."""
import json
import subprocess
import sys

def inspect(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height", "-show_entries",
        "format=duration", "-of", "json", path], text=True)
    data = json.loads(raw)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    return {"video_ok": video.get("codec_name") == "h264",
            "vertical_1080p": video.get("width") == 1080 and video.get("height") == 1920,
            "duration": float(data["format"]["duration"]),
            "audio_present": bool(audio),
            "narration_verified": False,
            "speech_subtitles_verified": False,
            "publication_approved": False}

if __name__ == "__main__":
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
