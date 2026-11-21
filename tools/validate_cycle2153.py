# cycle2153: image-slide video validation
# Run: python tools/validate_cycle2153.py path/to/video.mp4
import json, subprocess, sys
path = sys.argv[1]
probe = json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path]))
video = next(s for s in probe["streams"] if s["codec_type"] == "video")
assert (video["width"],video["height"]) == (1080,1920)
assert video["codec_name"] == "h264"
assert 11.9 <= float(probe["format"]["duration"]) <= 12.1
subprocess.run(["ffmpeg","-v","error","-i",path,"-f","null","-"],check=True)
print("PASS: resolution, codec, duration, full decode")
