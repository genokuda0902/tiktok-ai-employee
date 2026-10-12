"""Reusable ten-genre video QA; approval fails closed if Japanese narration is missing."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
GENRES = ("ai_work","beauty","psychology","saving","business","career","lifestyle","science","travel","comparison")
REQUIRED_WIDTH, REQUIRED_HEIGHT = 1080, 1920
def validate_timeline(rows, max_cps=9.0):
    if len(rows) < 2: raise ValueError("insufficient caption segments")
    end = 0.0
    for row in rows:
        start, stop = float(row["start"]), float(row["end"])
        if start < end-0.001 or stop <= start: raise ValueError("timeline overlap or invalid duration")
        if len(row["caption"])/(stop-start) > max_cps: raise ValueError("caption too fast")
        end = stop
    return end
def probe_video(path):
    p = subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height","-show_entries","format=duration","-of","json",str(path)],capture_output=True,text=True,check=True)
    obj=json.loads(p.stdout); video=next((s for s in obj["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in obj["streams"] if s["codec_type"]=="audio"),None)
    if not video or video.get("width")!=REQUIRED_WIDTH or video.get("height")!=REQUIRED_HEIGHT: raise ValueError("wrong video resolution")
    if video.get("codec_name")!="h264" or not audio or audio.get("codec_name")!="aac": raise ValueError("wrong codecs")
    return {"duration":float(obj["format"]["duration"]),"video":video,"audio":audio}
def approval_gate(*, japanese_voice_generated, voice_listening_approved, captions_synced, rights_cleared, employee_approved):
    return all((japanese_voice_generated,voice_listening_approved,captions_synced,rights_cleared,employee_approved))
def assert_publication_blocked_without_voice():
    assert not approval_gate(japanese_voice_generated=False,voice_listening_approved=True,captions_synced=True,rights_cleared=True,employee_approved=True)
if __name__=="__main__":
    import sys
    rows=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps({"timeline_seconds":validate_timeline(rows),"publication":"NOT_APPROVED"},ensure_ascii=False))
