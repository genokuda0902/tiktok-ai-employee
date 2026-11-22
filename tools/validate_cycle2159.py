"""Cycle2159 video validation: run python tools/validate_cycle2159.py VIDEO.mp4"""
import json, subprocess, sys
p=sys.argv[1]
probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height","-show_entries","format=duration","-of","json",p]))
streams=probe["streams"]
video=next(s for s in streams if s["codec_name"]=="h264")
assert (video["width"],video["height"])==(1080,1920)
assert abs(float(probe["format"]["duration"])-12)<0.1
assert any(s["codec_name"]=="aac" for s in streams)
subprocess.run(["ffmpeg","-v","error","-xerror","-i",p,"-f","null","-"],check=True)
print("PASS: resolution, duration, codecs, decode")
print("WARNING: audio stream is silent; Japanese TTS NOT validated")
