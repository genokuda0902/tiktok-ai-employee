"""Reusable chapter cue overlay for review-only vertical videos.

Run: python tools/cycle1203_scene_cue.py INPUT.mp4 OUTPUT.mp4
Requires ffmpeg. Does not authorize publishing input media.
"""
import subprocess
import sys
from pathlib import Path

def filtergraph(start=3.0, end=6.0):
    if not (0 <= start < end):
        raise ValueError("invalid cue interval")
    window = f"between(t,{start:g},{end:g})"
    return (f"drawbox=x=55:y=260:w=970:h=110:color=black@0.55:t=fill:enable='{window}',"
            f"drawbox=x=55:y=260:w=12:h=110:color=0x00d9c0:t=fill:enable='{window}'")

def render(source, target):
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    if Path(source).resolve() == Path(target).resolve():
        raise ValueError("input and output must differ")
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",str(source),
                    "-vf",filtergraph(),"-c:v","libx264","-preset","ultrafast",
                    "-crf","20","-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: cycle1203_scene_cue.py INPUT OUTPUT")
    render(sys.argv[1],sys.argv[2])
