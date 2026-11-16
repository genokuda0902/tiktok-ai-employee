"""Reusable gentle horizontal camera drift for portrait slide videos."""
import subprocess,sys
from pathlib import Path

def filtergraph(width=1080,height=1920,margin=12):
    if not (0 <= margin <= 32): raise ValueError('margin must be 0..32')
    if margin == 0: return 'null'
    return f"crop={width-2*margin}:{height-2*margin}:x='{2*margin}*n/(max(1,23*30))':y={margin},scale={width}:{height}:flags=lanczos,setsar=1"

def render(src,dst):
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(src),'-vf',filtergraph(),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True)
if __name__=='__main__': render(Path(sys.argv[1]),Path(sys.argv[2]))
