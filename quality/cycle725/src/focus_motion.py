#!/usr/bin/env python3
"""Zero-cost semantic LED circuit motion, over an existing review-only 1080x1920 MP4."""
import argparse, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
FPS=30; N=61; X,Y,W,H=90,600,830,300; START=11.033333
PALETTES={'AI・仕事効率化':'#61D6FF','美容・身だしなみ':'#FFB3CE','恋愛・心理':'#ED9BFF','お金・節約':'#78E4B2','営業・ビジネス':'#FFC86A','転職・キャリア':'#A9C1FF','健康・生活改善':'#83E0C9','雑学・科学':'#42E5D0','旅行・グルメ':'#FFA785','商品比較・暮らし':'#D0DCA5'}
def color(code,alpha):
    return tuple(bytes.fromhex(code[1:]))+(max(0,min(255,round(alpha))),)
def frame(i,genre='雑学・科学'):
    if i not in range(N) or genre not in PALETTES: raise ValueError('invalid frame/genre')
    t=i/(N-1); accent=PALETTES[genre]
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
    u=max(0,min(1,(t-.08)/.73));cx=130+570*u*u*(3-2*u);cy=134
    fade=math.sin(math.pi*min(1,max(0,t/.94)))**.6
    for r,a in [(42,16),(28,33),(17,76),(9,215)]:d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=color(accent,a*fade))
    glow=max(0,min(1,(t-.55)/.17))*max(0,min(1,(1.02-t)/.12))
    for r,a,width in [(90,35,10),(78,94,7),(64,176,5)]:d.arc((480-r,135-r,480+r,135+r),0,359,fill=color(accent,a*glow),width=width)
    for deg in (45,135,225,315):
        theta=math.radians(deg)
        d.line((480+82*math.cos(theta),135+82*math.sin(theta),480+98*math.cos(theta),135+98*math.sin(theta)),fill=color(accent,210*glow),width=5)
    return im
def run(cmd):
    p=subprocess.run(cmd,capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1000:])
def render(src,dst,genre='雑学・科学'):
    src,dst=Path(src),Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    mov=dst.parent/'cycle725_motion.mov'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate','30','-i','pipe:0','-frames:v',str(N),'-c:v','qtrle','-pix_fmt','argb',str(mov)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in range(N):p.stdin.write(frame(i,genre).tobytes())
    p.stdin.close();err=p.stderr.read();rc=p.wait()
    if rc:raise RuntimeError(err.decode(errors='replace')[-1000:])
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-itsoffset',f'{START:.6f}','-i',str(mov),'-filter_complex',f'[0:v][1:v]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v','605','-movflags','+faststart',str(dst)])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--genre',default='雑学・科学',choices=list(PALETTES));a=p.parse_args();render(a.input,a.output,a.genre)
