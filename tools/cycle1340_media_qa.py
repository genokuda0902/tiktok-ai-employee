"""Cross-genre fail-closed media checks for REVIEW ONLY outputs."""
import json
import subprocess

def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def check(path, *, min_width=1080, min_height=1920, require_audio=True):
    meta=probe(path)
    videos=[s for s in meta["streams"] if s.get("codec_type")=="video"]
    audio=[s for s in meta["streams"] if s.get("codec_type")=="audio"]
    issues=[]
    if not videos: issues.append("video_missing")
    elif int(videos[0].get("width",0))<min_width or int(videos[0].get("height",0))<min_height: issues.append("resolution_low")
    if require_audio and not audio: issues.append("audio_missing")
    duration=float(meta.get("format",{}).get("duration",0))
    if duration<=0: issues.append("duration_invalid")
    decoded=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True)
    if decoded.returncode: issues.append("decode_failed")
    return {"passed":not issues,"issues":issues,"duration":duration,"audio_present":bool(audio)}
