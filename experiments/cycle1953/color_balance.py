"""Reusable no-cost saturation guard for ten content genres."""
import argparse
import subprocess
from pathlib import Path

def filtergraph(saturation: float = 0.88) -> str:
    if not 0.5 <= saturation <= 1.0:
        raise ValueError("saturation must be within [0.5, 1.0]")
    return f"eq=saturation={saturation:.3f}"

def render(source: Path, output: Path, saturation: float = 0.88):
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(source),"-vf",filtergraph(saturation),"-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--saturation",type=float,default=0.88)
    a=p.parse_args()
    render(a.source,a.output,a.saturation)
