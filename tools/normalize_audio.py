"""Reusable audio loudness/peak guard for ten genre slide videos."""
import subprocess
from pathlib import Path

def normalize(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    subprocess.run([
        'ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-map','0:v:0','-map','0:a:0','-c:v','copy',
        '-af','loudnorm=I=-16:TP=-2:LRA=11',
        '-c:a','aac','-b:a','192k','-ar','48000',
        '-movflags','+faststart',str(target)
    ],check=True)

if __name__ == '__main__':
    import sys
    normalize(Path(sys.argv[1]),Path(sys.argv[2]))
