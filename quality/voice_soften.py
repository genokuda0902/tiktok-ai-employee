"""Gentle voice high-frequency smoothing for reusable video pipeline."""
import subprocess

def process(src, dst, gain_db=-1.2):
    if not -3.0 <= gain_db <= 0:
        raise ValueError("gain_db must be between -3 and 0")
    filters=f"equalizer=f=6500:t=h:width=2800:g={gain_db},volume=-3dB,alimiter=limit=0.65"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,
        "-map","0:v:0","-map","0:a:0","-c:v","copy","-af",filters,
        "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",dst],check=True)
