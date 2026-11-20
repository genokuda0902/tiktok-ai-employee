"""Apply a short fade-in to the first 300ms of narration, preserving video and outro."""
import subprocess

def build(source, destination):
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af","afade=t=in:st=0:d=0.30","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(destination)],check=True)
