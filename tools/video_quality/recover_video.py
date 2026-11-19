"""Recover slide video from last known visible source and reject black-frame regressions."""
import subprocess
import sys
from pathlib import Path

def recover(src, dst):
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),"-vf",
        "eq=contrast=1.025:brightness=0.005:saturation=1.04,format=yuv420p",
        "-c:v","libx264","-preset","veryfast","-crf","19",
        "-c:a","copy","-movflags","+faststart",str(dst)],check=True)

def verify(path):
    p=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-vf",
        "scale=54:96,signalstats,metadata=print:file=-",
        "-an","-f","null","-"],capture_output=True,text=True,check=True)
    values=[float(line.split("=",1)[1]) for line in p.stdout.splitlines()
            if "lavfi.signalstats.YAVG=" in line]
    if not values or sum(v<=18 for v in values)/len(values)>0.20:
        raise ValueError("black frame regression detected")
    return len(values), min(values), sum(values)/len(values)

if __name__=="__main__":
    src,dst=map(Path,sys.argv[1:3])
    recover(src,dst)
    print(verify(dst))
