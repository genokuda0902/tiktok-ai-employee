"""Reusable no-cost audio normalization for image-slide videos."""
import subprocess

def normalize(source, target, integrated_lufs=-16):
    if not -24 <= integrated_lufs <= -12:
        raise ValueError("integrated_lufs must be between -24 and -12")
    subprocess.run(["ffmpeg","-hide_banner","-nostdin","-y","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"loudnorm=I={integrated_lufs}:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(target)],check=True)
