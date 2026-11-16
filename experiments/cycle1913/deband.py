"""Reusable gentle gradient debanding for vertical videos."""
import subprocess

def render(src, dst, threshold=0.012):
    if not 0.001 <= threshold <= 0.03:
        raise ValueError("threshold outside safe range")
    cmd=["ffmpeg","-y","-i",str(src),"-vf",f"deband=1thr={threshold}:2thr={threshold}:3thr={threshold}:4thr={threshold}:range=12:blur=true","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dst)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
