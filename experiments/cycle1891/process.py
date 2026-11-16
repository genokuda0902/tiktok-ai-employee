"""10-genre reusable high-fidelity H.264 export, no new media assets."""
import subprocess
import sys
from pathlib import Path

def export(src, dst, crf=17):
    if not 0 <= crf <= 51:
        raise ValueError('CRF out of range')
    subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(src),'-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','medium','-crf',str(crf),'-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)],check=True)

if __name__ == '__main__':
    export(Path(sys.argv[1]),Path(sys.argv[2]))
