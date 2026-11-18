"""Reusable zero-cost audio true-peak guard for 10 genres; requires ffmpeg."""
import subprocess
from pathlib import Path

def render(source: str, destination: str):
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',source,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k',destination],check=True)

if __name__=='__main__':
    import sys
    render(sys.argv[1],sys.argv[2])
