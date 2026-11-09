"""Review-only MP4 technical gate. Does not authorize publication."""
import json
import subprocess
import sys

def probe(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def validate(path):
    data=probe(path)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    if not video: raise ValueError("missing video")
    if video["width"]<720 or video["height"]<1280: raise ValueError("resolution below review floor")
    if not 10 <= float(data["format"]["duration"]) <= 45: raise ValueError("unexpected duration")
    subprocess.run(["ffmpeg","-v","error","-i",path,"-f","null","-"],check=True)
    return {"duration":float(data["format"]["duration"]),"width":video["width"],"height":video["height"],"audio_present":any(s["codec_type"]=="audio" for s in data["streams"]),"publication_approved":False}

if __name__=="__main__":
    print(json.dumps(validate(sys.argv[1]),ensure_ascii=False))
