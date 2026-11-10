"""Run: python tests/test_cycle1601.py output.mp4"""
import json
import subprocess
import sys
p = sys.argv[1]
d = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p]))
v = next(s for s in d["streams"] if s["codec_type"] == "video")
a = next(s for s in d["streams"] if s["codec_type"] == "audio")
assert (v["width"], v["height"]) == (1080, 1920)
assert v["codec_name"] == "h264" and a["codec_name"] == "aac"
assert float(d["format"]["duration"]) > 20
with open(p, "rb") as f:
    b = f.read()
assert b.index(b"moov") < b.index(b"mdat")
subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "null", "-"], check=True)
print("PASS")
