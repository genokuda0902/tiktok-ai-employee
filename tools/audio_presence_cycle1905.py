"""Reusable speech-presence polish for 10 genre slide videos. Review only."""
import subprocess

def render(src: str, dst: str):
    cmd=['ffmpeg','-hide_banner','-y','-i',src,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af','equalizer=f=2600:t=q:w=1.0:g=1.5','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',dst]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
