"""Selective upper-area sharpening for vertical image slides."""
import subprocess

def render(source, target):
    vf = "split=2[top][base];[top]crop=iw:1380:0:0,unsharp=5:5:0.35:3:3:0[sharp];[base][sharp]overlay=0:0:format=auto,format=yuv420p"
    subprocess.run(["ffmpeg","-y","-i",str(source),"-filter_complex",vf,"-map","0:a:0","-c:v","libx264","-crf","19","-c:a","copy",str(target)],check=True)
