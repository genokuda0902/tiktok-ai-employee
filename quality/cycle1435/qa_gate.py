# cycle1435: safe-zone and legibility gate
# Review-only. No speech or publication approval claimed.
from pathlib import Path
import subprocess,json

def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def validate(path, narration_verified=False, employee_approved=False):
    data=probe(path)
    videos=[s for s in data["streams"] if s["codec_type"]=="video"]
    audios=[s for s in data["streams"] if s["codec_type"]=="audio"]
    technical=bool(videos and audios and videos[0]["width"]==1080 and videos[0]["height"]==1920)
    return {"technical_pass":technical,"japanese_narration_verified":narration_verified,"employee_approved":employee_approved,"publication_approved":bool(technical and narration_verified and employee_approved)}
