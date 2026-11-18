"""Sharpen illustration only; keep caption band and original audio."""
import subprocess
import sys
from pathlib import Path

def render(src, dst):
    filtergraph = ('[0:v]split=2[base][top];'
                   '[top]crop=1080:1248:0:0,unsharp=5:5:0.45:5:5:0[sharp];'
                   '[base][sharp]overlay=0:0:format=auto,format=yuv420p[out]')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                    '-i',str(src),'-filter_complex',filtergraph,
                    '-map','[out]','-map','0:a:0','-c:v','libx264',
                    '-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
                    '-c:a','copy','-movflags','+faststart',str(dst)],check=True)
if __name__ == '__main__':
    render(Path(sys.argv[1]), Path(sys.argv[2]))
