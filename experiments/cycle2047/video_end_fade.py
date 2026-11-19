"""Reusable end-of-video visual fade; preserves audio."""
import json, subprocess, sys

def duration(path):
    d=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",path]))
    return float(d["format"]["duration"])

def fade_filter(seconds, fade=0.6):
    if not 0 < fade < seconds: raise ValueError("invalid fade duration")
    return f"fade=t=out:st={seconds-fade:.3f}:d={fade:.3f}"

def render(source, target, fade=0.6):
    subprocess.run(["ffmpeg","-y","-i",source,"-vf",fade_filter(duration(source),fade),"-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",target],check=True)

if __name__=="__main__": render(sys.argv[1],sys.argv[2])
