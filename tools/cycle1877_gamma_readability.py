"""Mild gamma lift for dark Japanese slideshow readability; audio copied untouched."""
import subprocess

def improve(src, dst):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-vf","eq=gamma=1.09:brightness=0.008:saturation=1.02","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
