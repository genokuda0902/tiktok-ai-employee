"""Optional subtle detail enhancement; input path is caller supplied."""
import argparse
import subprocess

def enhance(src, dst):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,
      "-vf","unsharp=3:3:0.35:3:3:0.0","-c:v","libx264",
      "-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
      "-c:a","copy","-movflags","+faststart",dst],check=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input");p.add_argument("output")
    a=p.parse_args();enhance(a.input,a.output)
