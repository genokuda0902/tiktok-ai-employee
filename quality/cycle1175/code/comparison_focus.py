#!/usr/bin/env python3
"""Review-only two-stage Before/After focus. No posting or media upload."""
from __future__ import annotations
import subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
PALETTES={
 'ai':('#e87caa','#51d9d1'), 'business':('#ed9c7a','#55d1c5'),
 'money':('#ed9b8b','#83d9ac'), 'learning':('#e58aab','#6ac8ed'),
 'health':('#ec8c9a','#67dcb3'), 'food':('#e89e88','#e2c87a'),
 'travel':('#ec9c83','#7abfe9'), 'beauty':('#e7a0c6','#9bc7f2'),
 'career':('#e89e88','#67d3ca'), 'life':('#e89f98','#9fd6ad')}
DEFAULT_CARDS={'before':(91,550,838,722),'after':(91,794,838,1005)}

def validate(width,height,cards=DEFAULT_CARDS,genre='ai'):
    if genre not in GENRES: raise ValueError('unknown genre')
    if (width,height)!=(1080,1920): raise ValueError('requires 1080x1920 template')
    for name in ('before','after'):
        x0,y0,x1,y1=cards[name]
        if not (0<=x0<x1<width and 0<=y0<y1<1320):
            raise ValueError('invalid geometry / subtitle overlap')

def render_glow(size,bounds,color):
    w,h=size; validate(w,h)
    x0,y0,x1,y1=bounds
    rgb=tuple(bytes.fromhex(color[1:]))
    halo=Image.new('RGBA',(w,h),(0,0,0,0))
    ImageDraw.Draw(halo).rounded_rectangle(
        (x0-5,y0-5,x1+5,y1+5),radius=25,outline=rgb+(130,),width=9)
    base=halo.filter(ImageFilter.GaussianBlur(13))
    ImageDraw.Draw(base).rounded_rectangle(
        (x0-2,y0-2,x1+2,y1+2),radius=22,outline=rgb+(155,),width=4)
    return base

def filter_graph(before_start,before_end,after_start,after_end,fade=.2):
    if not (0<=before_start<before_end<=after_start<after_end):
        raise ValueError('windows overlap')
    if min(before_end-before_start,after_end-after_start)<=fade*2:
        raise ValueError('focus window too short')
    return (
      f'[1:v]format=rgba,fade=t=in:st={before_start}:d={fade}:alpha=1,'
      f'fade=t=out:st={before_end-fade}:d={fade}:alpha=1[bf];'
      f'[2:v]format=rgba,fade=t=in:st={after_start}:d={fade}:alpha=1,'
      f'fade=t=out:st={after_end-fade}:d={fade}:alpha=1[af];'
      '[0:v][bf]overlay=0:0:shortest=1:format=auto[tmp];'
      '[tmp][af]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]')

def frame_count(src):
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
       '-show_entries','stream=nb_frames','-of',
       'default=noprint_wrappers=1:nokey=1',str(src)],
       capture_output=True,text=True,check=True)
    return int(p.stdout.strip())

def run(src,dst,*,genre='ai',before_start=13.93,before_end=15.03,
        after_start=15.12,after_end=16.49,cards=DEFAULT_CARDS):
    src,dst=Path(src),Path(dst)
    validate(1080,1920,cards,genre)
    if src.resolve()==dst.resolve(): raise ValueError('source overwrite refused')
    if not src.is_file(): raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        paths=[]
        for key,color in zip(('before','after'),PALETTES[genre]):
            p=Path(td)/(key+'.png')
            render_glow((1080,1920),cards[key],color).save(p)
            paths.append(p)
        cmd=['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
          '-i',str(src),'-loop','1','-framerate','30','-i',str(paths[0]),
          '-loop','1','-framerate','30','-i',str(paths[1]),
          '-filter_complex',filter_graph(before_start,before_end,after_start,after_end),
          '-map','[v]','-map','0:a?','-map_metadata','0','-map_chapters','0',
          '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
          '-c:a','copy','-movflags','+faststart','-frames:v',str(frame_count(src)),
          str(dst)]
        subprocess.run(cmd,check=True)
