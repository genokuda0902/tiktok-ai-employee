"""Review-only caption burn-in. Source media and subtitles are explicitly supplied."""
import json
import subprocess
from pathlib import Path

def render(source, captions, output):
    source, captions, output = map(Path, (source, captions, output))
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("source or captions missing")
    style = "FontName=Noto Sans CJK JP,FontSize=24,PrimaryColour=&H00FFFFFF,BorderStyle=3,BackColour=&H99000000,MarginV=210,Alignment=2"
    vf = "subtitles=" + str(captions.resolve()).replace(":", r"\:") + ":force_style='" + style + "'"
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",vf,"-c:v","libx264","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(output)],check=True)

def gate(probe):
    streams = probe["streams"]
    video = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = any(s["codec_type"] == "audio" for s in streams)
    return {"video_present": bool(video), "vertical_720_min": bool(video and video["width"] >= 720 and video["height"] >= 1280), "audio_present": audio, "japanese_narration_verified": False, "speech_caption_sync_verified": False, "publication_approved": False}
