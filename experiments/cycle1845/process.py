"""Reusable zero-cost AAC peak guard for short-form videos."""
import subprocess
from pathlib import Path

def peak_guard(source: str, target: str, limit: float = 0.68):
    if not 0.1 <= limit <= 0.9:
        raise ValueError('limit must be between 0.1 and 0.9')
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',source,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',f'alimiter=limit={limit}:attack=5:release=80:level=false','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',target],check=True)
