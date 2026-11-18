"""Fail-closed verification for original review-only vertical MP4s."""
import json, subprocess

def inspect(path, narration_verified=False, captions_aligned=False, assets_approved=False, employee_approved=False):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    technical=bool(video and video.get("width",0)>=720 and video.get("height",0)>=1280)
    speech=bool(audio and narration_verified)
    return {"technical_vertical":technical,"audio_present":bool(audio),"japanese_narration_verified":speech,"speech_caption_alignment_verified":bool(speech and captions_aligned),"assets_approved":bool(assets_approved),"employee_approved":bool(employee_approved),"publication_allowed":bool(technical and speech and captions_aligned and assets_approved and employee_approved)}
