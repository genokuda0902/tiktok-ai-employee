"""Cross-genre, review-only video QA. Never treats an audio track as Japanese narration."""
import json
import subprocess
import sys
from pathlib import Path

def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def assess(path, narration_verified=False, captions_synced=False, employee_approved=False):
    data=probe(path)
    streams=data["streams"]
    video=next((s for s in streams if s["codec_type"]=="video"),{})
    audio=next((s for s in streams if s["codec_type"]=="audio"),None)
    dimensions=(video.get("width"),video.get("height"))
    decode=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True)
    return {
        "dimensions":dimensions,
        "duration":float(data["format"]["duration"]),
        "video_codec":video.get("codec_name"),
        "audio_codec":audio.get("codec_name") if audio else None,
        "full_decode_pass":decode.returncode==0,
        "narration_verified":bool(narration_verified),
        "captions_synced":bool(captions_synced),
        "employee_approved":bool(employee_approved),
        "publication_approved":bool(decode.returncode==0 and dimensions==(1080,1920) and narration_verified and captions_synced and employee_approved),
    }

if __name__=="__main__":
    print(json.dumps(assess(Path(sys.argv[1])),ensure_ascii=False,indent=2))
