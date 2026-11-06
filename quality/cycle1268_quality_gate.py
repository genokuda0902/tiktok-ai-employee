"""Cycle 1268: fail-closed QA for review-only MP4 and timed scene captions."""
import json
import subprocess
from pathlib import Path

def probe(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def inspect(path, expected_scenes=3):
    data=probe(path)
    streams=data["streams"]
    videos=[s for s in streams if s["codec_type"]=="video"]
    audio=[s for s in streams if s["codec_type"]=="audio"]
    duration=float(data["format"]["duration"])
    result={"duration":duration,"video":bool(videos),"audio":bool(audio),"resolution":[videos[0]["width"],videos[0]["height"]] if videos else None}
    result["posting_allowed"]=False
    result["quality_approved"]=False
    result["failures"]=[]
    if not videos: result["failures"].append("VIDEO_MISSING")
    if not audio: result["failures"].append("JAPANESE_NARRATION_UNVERIFIED")
    if not (11.5<=duration<=12.5): result["failures"].append("DURATION_OUT_OF_RANGE")
    if result["resolution"] != [1080,1920]: result["failures"].append("RESOLUTION_MISMATCH")
    result["failures"].append("HUMAN_APPROVAL_REQUIRED")
    return result
