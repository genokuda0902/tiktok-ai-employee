"""Fail-closed QA: a present audio stream is not proof of Japanese speech."""
import json
import subprocess
import sys

def probe(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                        "-show_format", "-of", "json", path],
                       capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def validate(path):
    data = probe(path)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    if not video or video["width"] < 720 or video["height"] < 1280:
        raise ValueError("vertical video missing or below 720x1280")
    if not audio:
        raise ValueError("audio track missing")
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"], check=True)
    return {"video": "PASS", "audio_stream": "PRESENT",
            "japanese_narration": "NOT_VERIFIED",
            "speech_caption_sync": "NOT_VERIFIED",
            "publication_approved": False}

if __name__ == "__main__":
    print(json.dumps(validate(sys.argv[1]), ensure_ascii=False, indent=2))
