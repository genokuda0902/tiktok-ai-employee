import json, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1])
data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height","-show_entries","format=duration","-of","json",str(p)]))
v=[s for s in data["streams"] if s["codec_type"]=="video"]
a=[s for s in data["streams"] if s["codec_type"]=="audio"]
assert len(v)==1 and v[0]["codec_name"]=="h264"
assert (v[0]["width"],v[0]["height"])==(1080,1920)
assert abs(float(data["format"]["duration"])-12)<0.1
assert not a, "Audio unexpectedly present; Japanese narration requires separate verification"
subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","null","-"],check=True)
print("TECHNICAL PASS; JAPANESE NARRATION MISSING; PUBLICATION_NOT_APPROVED")
