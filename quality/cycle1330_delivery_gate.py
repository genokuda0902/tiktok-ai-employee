"""Cross-genre MP4 delivery gate: reject silent videos and unreadable dimensions."""
import json
import subprocess
import sys

def probe(path):
    result = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def validate(data):
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    problems=[]
    if not video: problems.append("missing video")
    elif int(video.get("width",0))<1080 or int(video.get("height",0))<1920: problems.append("below 1080x1920")
    if not audio: problems.append("missing narration/audio stream")
    if float(data.get("format",{}).get("duration",0))<=0: problems.append("invalid duration")
    return problems

if __name__=="__main__":
    problems=validate(probe(sys.argv[1]))
    print(json.dumps({"passed":not problems,"issues":problems},ensure_ascii=False))
    sys.exit(bool(problems))
