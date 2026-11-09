#!/usr/bin/env python3
"""Match the final 0.55 seconds of audio to the existing visual end fade.
Requires ffmpeg/ffprobe; no paid dependencies. For all genre templates.
"""
import json, subprocess, sys
from pathlib import Path

def duration(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-of","json",str(path)]))
    return float(data["format"]["duration"])

def render(src,dst,fade=0.55):
    length=duration(src)
    assert 0 < fade < length
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(src),
        "-map","0","-c","copy","-c:a","aac","-b:a","160k",
        "-af",f"afade=t=out:st={length-fade:.3f}:d={fade}",
        "-movflags","+faststart",str(dst)],check=True)
    return duration(dst)

if __name__=="__main__":
    if len(sys.argv)!=3: sys.exit("usage: audio_end_fade.py INPUT.mp4 OUTPUT.mp4")
    render(Path(sys.argv[1]),Path(sys.argv[2]))
