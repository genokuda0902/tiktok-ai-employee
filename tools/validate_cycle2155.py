# cycle2155 subtitle burn validation
import json, subprocess, sys
p=sys.argv[1]
d=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p]))
v=next(s for s in d["streams"] if s["codec_type"]=="video")
assert (v["width"],v["height"],v["codec_name"]) == (1080,1920,"h264")
assert 11.9<float(d["format"]["duration"])<12.1
assert any(s["codec_type"]=="audio" and s["codec_name"]=="aac" for s in d["streams"])
subprocess.run(["ffmpeg","-v","error","-i",p,"-f","null","-"],check=True)
print("PASS: structural and decode checks; Japanese narration NOT validated")
