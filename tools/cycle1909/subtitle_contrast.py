"""Reusable subtitle-zone contrast overlay for review videos."""
import argparse
import subprocess

def filtergraph(width=1080, height=1920, opacity=0.22):
    if not 0 <= opacity <= 0.5:
        raise ValueError("opacity must be between 0 and 0.5")
    return f"drawbox=x=0:y={round(height*.805)}:w={width}:h={round(height*.105)}:color=black@{opacity}:t=fill"

def render(src, dst, opacity=0.22):
    subprocess.run(["ffmpeg","-y","-i",str(src),"-vf",filtergraph(opacity=opacity),"-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dst)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("src");p.add_argument("dst");p.add_argument("--opacity",type=float,default=.22)
    a=p.parse_args();render(a.src,a.dst,a.opacity)
