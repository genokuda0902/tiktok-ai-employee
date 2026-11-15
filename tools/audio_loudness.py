"""Zero-cost audio loudness normalization; preserves video bitstream."""
import subprocess
from pathlib import Path

def normalize(src: str, dst: str, target=-16.0):
    if not -24 <= target <= -12:
        raise ValueError("target LUFS outside safe configured range")
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg","-hide_banner","-nostdin","-y","-i",src,
           "-map","0:v:0","-map","0:a:0","-c:v","copy",
           "-af",f"loudnorm=I={target}:TP=-1.5:LRA=11",
           "-c:a","aac","-b:a","192k","-ar","48000",
           "-movflags","+faststart",dst]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return dst
