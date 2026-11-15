"""Reusable audio tail fade for 10 genre slide videos; keeps video bitstream intact."""
import argparse
import json
import subprocess

def duration(path):
    p = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",path],capture_output=True,text=True,check=True)
    return float(json.loads(p.stdout)["format"]["duration"])

def process(src,dst,fade=0.45):
    d=duration(src)
    if d <= fade: raise ValueError("fade must be shorter than video")
    subprocess.run(["ffmpeg","-y","-i",src,"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=out:st={d-fade:.3f}:d={fade:.3f}","-c:a","aac","-b:a","192k","-movflags","+faststart",dst],check=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("src");p.add_argument("dst");p.add_argument("--fade",type=float,default=.45)
    a=p.parse_args();process(a.src,a.dst,a.fade)
