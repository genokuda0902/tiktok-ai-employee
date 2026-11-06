"""Fail-closed review gate for generated MP4; no publication approval implied."""
import json
import subprocess

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    streams=data["streams"]
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    duration=float(data["format"].get("duration",0))
    decode=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True,text=True)
    return {"video_ok": bool(video and video.get("codec_name")=="h264" and video.get("width")==1080 and video.get("height")==1920 and 10<=duration<=45 and decode.returncode==0), "audio_present":bool(audio), "japanese_narration_verified":False,"speech_caption_sync_verified":False,"publish_approved":False,"duration":duration,"decode_errors":decode.stderr}
