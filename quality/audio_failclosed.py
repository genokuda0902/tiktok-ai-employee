"""Reject review-only MP4s without audio, Japanese subtitles, or vertical video."""
import json
import subprocess
import sys

def inspect(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",path]))
    streams=data["streams"]
    videos=[s for s in streams if s["codec_type"]=="video"]
    audios=[s for s in streams if s["codec_type"]=="audio"]
    errors=[]
    if not videos or (videos[0]["width"],videos[0]["height"])!=(1080,1920):
        errors.append("expected 1080x1920 video")
    if not audios:
        errors.append("missing narration audio stream")
    return errors

if __name__=="__main__":
    errors=inspect(sys.argv[1])
    print(json.dumps({"publishable":not errors,"errors":errors},ensure_ascii=False))
    sys.exit(2 if errors else 0)
