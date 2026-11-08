"""Fail-closed review gate for rendered TikTok clips; stdlib only."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True))
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    duration=float(data.get("format",{}).get("duration",0))
    return {"video_present":bool(video),"audio_present":bool(audio),"width":video.get("width") if video else None,"height":video.get("height") if video else None,"duration":duration}

def publishable(meta, approved=False):
    return bool(approved and meta["video_present"] and meta["audio_present"] and meta["width"]>=1080 and meta["height"]>=1920 and meta["duration"]>0)

if __name__=="__main__":
    import sys
    report=inspect(Path(sys.argv[1]))
    report["publication_approved"]=publishable(report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
