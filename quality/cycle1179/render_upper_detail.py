"""Reimplementation: mild detail enhancement above the subtitle safe region."""
import argparse
import subprocess
from pathlib import Path

def filtergraph(width=1080, height=1920, safe_bottom=570, amount=0.55):
    if not (0 < safe_bottom < height) or not (0 <= amount <= 1):
        raise ValueError("invalid safe region or sharpening amount")
    upper = height - safe_bottom
    return (f"[0:v]split=2[top][bottom];"
            f"[top]crop={width}:{upper}:0:0,unsharp=5:5:{amount}:5:5:0.0[t];"
            f"[bottom]crop={width}:{safe_bottom}:0:{upper}[b];"
            f"[t][b]vstack=inputs=2[v]")

def render(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
                    "-filter_complex",filtergraph(),"-map","[v]","-map","0:a:0",
                    "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
                    "-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    render(args.source,args.target)
