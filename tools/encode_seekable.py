"""Reusable 10-category TikTok slideshow delivery encoder. Requires ffmpeg."""
import subprocess
from pathlib import Path

def encode(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-force_key_frames','expr:gte(t,n_forced*2)','-c:a','copy','-movflags','+faststart',str(target)]
    subprocess.run(cmd, check=True)
    return target
