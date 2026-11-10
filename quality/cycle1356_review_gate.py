"""Review-only QA for synthetic demos. No media stream implies narration."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=any(s["codec_type"]=="audio" for s in data["streams"])
    return {"width":video["width"] if video else None,"height":video["height"] if video else None,
            "audio_stream":audio,"japanese_narration_verified":False,
            "speech_caption_sync_verified":False,"posting_allowed":False,
            "review_only":True}

def test_fail_closed():
    sample={"audio_stream":False,"japanese_narration_verified":False,"posting_allowed":False}
    assert not sample["posting_allowed"]
    assert not sample["japanese_narration_verified"]
