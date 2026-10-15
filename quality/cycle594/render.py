"""Local MP4 build. Input cycle593 baseline must be provided by operator."""
import argparse,subprocess
from pathlib import Path
from card import draw_overlay
def build(src,out,genre):
    src,out=Path(src),Path(out)
    if not src.is_file():raise FileNotFoundError(src)
    out.parent.mkdir(parents=True,exist_ok=True)
    overlay=out.with_suffix('.overlay.png')
    draw_overlay(genre,overlay)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
      '-loop','1','-framerate','30','-i',str(overlay),
      '-filter_complex','[1:v]format=rgba,fade=t=in:st=13.90:d=0.20:alpha=1[ov];[0:v][ov]overlay=x=0:y=0:format=auto:shortest=1[v]',
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
      '-pix_fmt','yuv420p','-r','30','-frames:v','468','-c:a','copy','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='雑学・科学')
    a=p.parse_args();build(a.input,a.output,a.genre)
