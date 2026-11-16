"""Subtle luma sharpening; chroma unchanged; preserve audio stream."""
import argparse
import subprocess

def command(src, dst, strength=0.35):
    if not 0 <= strength <= 1:
        raise ValueError("strength must be in [0,1]")
    return ["ffmpeg","-y","-i",src,"-vf",f"unsharp=3:3:{strength}:3:3:0.0","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",dst]

if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("src");p.add_argument("dst");p.add_argument("--strength",type=float,default=0.35)
    a=p.parse_args();subprocess.run(command(a.src,a.dst,a.strength),check=True)
