"""Reusable audio loudness pass for vertical MP4s."""
import subprocess
from pathlib import Path

def normalize(source: Path, target: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(target)],check=True)
