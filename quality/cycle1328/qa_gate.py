"""Shared QA gate for review-only TikTok MP4s. Requires ffprobe on PATH."""
import json, subprocess, sys
from pathlib import Path

def inspect(path):
    result = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(result.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    issues=[]
    if not video or int(video.get("width",0))<1080 or int(video.get("height",0))<1920: issues.append("resolution_below_1080x1920")
    if not audio: issues.append("missing_narration_audio")
    if float(data["format"].get("duration",0))<=0: issues.append("invalid_duration")
    return {"approved":not issues,"issues":issues,"duration":float(data["format"].get("duration",0))}

if __name__=="__main__":
    report=inspect(Path(sys.argv[1]));print(json.dumps(report,ensure_ascii=False));sys.exit(0 if report["approved"] else 2)
