"""Add genre-neutral timed visual beats to an existing review MP4. No posting."""
from pathlib import Path
import argparse
import subprocess

BEATS = ((4, 5.5, "0x38bdf8"), (8, 9.5, "0xfbbf24"), (16, 17.5, "0x34d399"))

def make_filter(beats=BEATS):
    if any(a < 0 or b <= a for a,b,_ in beats):
        raise ValueError("invalid timing")
    if any(beats[i][1] > beats[i+1][0] for i in range(len(beats)-1)):
        raise ValueError("overlapping beats")
    return ",".join(
        f"drawbox=x=104:y=300:w=872:h=10:color={color}@0.9:t=fill:enable='between(t,{start},{end})'"
        for start,end,color in beats
    )

def render(source: Path, target: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf",make_filter(),"-map","0:v:0","-map","0:a:0",
        "-c:v","libx264","-preset","ultrafast","-crf","24",
        "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)
    ], check=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("source",type=Path)
    parser.add_argument("target",type=Path)
    args=parser.parse_args()
    render(args.source,args.target)
