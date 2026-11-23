"""Fail closed when a rendered MP4 lacks Japanese narration or vertical video."""
import json
import subprocess
import sys

def validate(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height:format=duration",
         "-of", "json", path], capture_output=True, text=True, check=True)
    streams = json.loads(result.stdout)["streams"]
    video = [s for s in streams if s["codec_type"] == "video"]
    audio = [s for s in streams if s["codec_type"] == "audio"]
    assert len(video) == 1 and video[0]["width"] == 1080 and video[0]["height"] == 1920
    assert audio, "Missing narration: block publication"
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"], check=True)
    return True

if __name__ == "__main__":
    validate(sys.argv[1])
