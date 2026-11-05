"""Reusable FFmpeg audio-level QA for review-only videos (not speech validation)."""
import json
import subprocess
from pathlib import Path


def probe_audio(path):
    p = subprocess.run(["ffprobe","-v","error","-select_streams","a:0",
        "-show_entries","stream=codec_name,sample_rate,channels", "-of","json",str(path)],
        check=True,capture_output=True,text=True)
    streams=json.loads(p.stdout).get("streams",[])
    if not streams:
        raise ValueError("Audio stream missing")
    return streams[0]


def render_review(source, destination):
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    probe_audio(source)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf","eq=contrast=1.07:saturation=1.08,format=yuv420p",
        "-af","loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v","libx264","-preset","veryfast","-crf","24",
        "-c:a","aac","-b:a","128k","-movflags","+faststart",str(destination)],check=True)
    probe_audio(destination)
    return destination

# This checks audio presence and processing only, NOT Japanese speech,
# caption synchronization, loudness measurement, or publishing rights.
