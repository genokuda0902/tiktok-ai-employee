#!/usr/bin/env python3
"""Zero-cost reusable audio clarity pass. REVIEW_ONLY; no publishing."""
import argparse
import json
import subprocess
from pathlib import Path

FILTER = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11"

def build(src: Path, dst: Path):
    if not src.is_file() or src.stat().st_size == 0:
        raise ValueError("Input MP4 is missing or empty")
    if src.resolve() == dst.resolve():
        raise ValueError("Never overwrite source")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),
        "-map","0:v:0","-map","0:a:0","-c:v","copy",
        "-af",FILTER,"-c:a","aac","-b:a","160k","-ar","48000",
        "-metadata:s:a:0","language=jpn","-movflags","+faststart",str(dst)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(dst),"-f","null","-"],check=True)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(dst)]))
    streams=probe["streams"]
    assert any(s.get("codec_name")=="h264" for s in streams)
    assert any(s.get("codec_name")=="aac" and s.get("sample_rate")=="48000" for s in streams)
    assert 22.9 < float(probe["format"]["duration"]) < 23.2, "Unexpected duration"
    return probe

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path);p.add_argument("output",type=Path)
    a=p.parse_args()
    build(a.input,a.output)
