"""Review-only video delivery gate: no silent or unverified speech passes publication."""
import json
import subprocess

def inspect(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
    streams=data["streams"]
    video=next(s for s in streams if s["codec_type"]=="video")
    audio=any(s["codec_type"]=="audio" for s in streams)
    return {"width":video["width"],"height":video["height"],"duration":float(data["format"]["duration"]),"has_audio":audio,"japanese_narration_verified":False,"publication_approved":False}

def publishable(result):
    return result["width"]>=720 and result["height"]>=1280 and result["has_audio"] and result["japanese_narration_verified"] and result["publication_approved"]
