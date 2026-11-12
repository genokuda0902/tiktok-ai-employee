import json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1]);assert p.is_file() and p.stat().st_size>100000
r=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)]))
v=next(x for x in r["streams"] if x["codec_type"]=="video")
a=next(x for x in r["streams"] if x["codec_type"]=="audio")
assert (v["width"],v["height"],v["codec_name"])==(1080,1920,"h264")
assert a["codec_name"]=="aac" and 22<float(r["format"]["duration"])<24
subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(p),"-f","null","-"],check=True)
print("PASS")
