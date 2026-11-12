"""Reusable zero-cost synchronized opening fade for slide videos."""
import argparse, subprocess
def render(src,dst,fade=0.35):
    if not 0.1<=fade<=1.0: raise ValueError("fade out of range")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,"-vf",f"fade=t=in:st=0:d={fade}","-af",f"afade=t=in:st=0:d={fade}","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",dst],check=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("src");p.add_argument("dst");p.add_argument("--fade",type=float,default=0.35);a=p.parse_args();render(a.src,a.dst,a.fade)
