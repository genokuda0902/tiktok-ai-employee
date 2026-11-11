"""Fail-closed review gate for all genres: an audio stream is not narration."""
import json, subprocess

def probe(path):
    result=subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True)
    return json.loads(result)

def assess(info, narration_verified=False, timed_captions_verified=False, employee_approved=False):
    streams=info.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=any(s.get("codec_type")=="audio" for s in streams)
    resolution=bool(video and video.get("width")==1080 and video.get("height")==1920)
    return {"resolution_ok":resolution,"audio_stream_present":audio,"narration_verified":bool(audio and narration_verified),"timed_captions_verified":bool(timed_captions_verified),"employee_approved":bool(employee_approved),"publication_approved":bool(resolution and audio and narration_verified and timed_captions_verified and employee_approved)}
