"""Review-only audio filter for local videos. No media upload."""
import subprocess
from pathlib import Path

FILTER = 'highpass=f=80,lowpass=f=12000,alimiter=limit=0.89:attack=5:release=80'

def command(source: Path, destination: Path):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError('input and output must differ')
    if source.suffix.lower() != '.mp4' or destination.suffix.lower() != '.mp4':
        raise ValueError('MP4 files only')
    return ['ffmpeg','-hide_banner','-y','-i',str(source),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',FILTER,'-c:a','aac','-b:a','128k','-movflags','+faststart',str(destination)]

def render(source: Path, destination: Path):
    subprocess.run(command(source, destination), check=True)
