"""Reusable audio loudness finishing for vertical slide videos (10 genres)."""
import json, subprocess, sys
def call(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def duration(path):
    return float(json.loads(call(["ffprobe","-v","error","-show_entries","format=duration","-of","json",path]))["format"]["duration"])
def finish(src, dst):
    d=duration(src)
    assert d>1
    af=f"loudnorm=I=-16:TP=-2:LRA=9,afade=t=out:st={d-.65:.3f}:d=.65"
    subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",af,"-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",dst],check=True)
if __name__=="__main__": finish(sys.argv[1],sys.argv[2])
