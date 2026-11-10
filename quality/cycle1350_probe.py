"""Shared fail-closed MP4 quality probe. Does not infer narration from an audio stream."""
import json, subprocess
from pathlib import Path

def probe(path):
    p=Path(path)
    if not p.is_file(): raise FileNotFoundError(p)
    run=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)],capture_output=True,text=True,check=True)
    data=json.loads(run.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    if video is None: raise ValueError("missing video")
    decode=subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","null","-"],capture_output=True,text=True)
    return {"width":video["width"],"height":video["height"],"duration":float(data["format"]["duration"]),
            "audio_stream_present":audio is not None,"japanese_narration_verified":False,
            "speech_synced_captions_verified":False,"decode_ok":decode.returncode==0,
            "publication_approved":False}
