#!/usr/bin/env python3
"""Free/offline opening-hook focus animation for captioned vertical videos.

Uses transparent overlays, not synthetic speech or third-party visual assets.
AAC is copied, and the subtitle region is untouched.
Per-genre palette reusable; geometry requires review for each new genre.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import math
import subprocess
from PIL import Image, ImageDraw, ImageFilter

WIDTH, HEIGHT, FPS = 1080, 1920, 30
GENRE_COLORS = {
    'ai': ('#F2C966', '#59E4D6'),
    'business': ('#EAC37D', '#8EC5FF'),
    'money': ('#F4D57B', '#63E5B8'),
    'learning': ('#F4CA72', '#A7C4FF'),
    'health': ('#F1D47B', '#74E4C4'),
    'food': ('#F7BD79', '#A9E69B'),
    'travel': ('#F5D38C', '#78D6F0'),
    'beauty': ('#F5CBBD', '#D5B6F7'),
    'career': ('#F2D28A', '#82C4F8'),
    'life': ('#F3D193', '#98E0C5'),
}

@dataclass(frozen=True)
class HookGeometry:
    underline: tuple[int,int,int] = (74, 455, 605)
    focal: tuple[int,int] = (540, 870)
    subtitle_top: int = 1150
    frame_count: int = 42

def validate(geometry: HookGeometry, genre: str):
    if genre not in GENRE_COLORS: raise ValueError('unsupported genre')
    x0,y,x1=geometry.underline
    cx,cy=geometry.focal
    if not (0<=x0<x1<WIDTH and 50<y<geometry.subtitle_top-120):
        raise ValueError('underline outside safe story region')
    if not (80<=cx<=WIDTH-80 and 80<=cy<=geometry.subtitle_top-90):
        raise ValueError('focus pulse overlaps safe subtitle area')
    if not (24<=geometry.frame_count<=45):
        raise ValueError('opening effect must end before first scene cut')
    return True

def ease(t: float) -> float:
    t=max(0.0,min(1.0,t))
    return t*t*(3-2*t)

def rgba(hex_color: str, alpha: int):
    c=hex_color.lstrip('#')
    return tuple(int(c[i:i+2],16) for i in (0,2,4))+(max(0,min(255,alpha)),)

def draw_frame(idx: int, genre='ai', geometry=HookGeometry()) -> Image.Image:
    validate(geometry,genre)
    if not 0<=idx<geometry.frame_count: raise ValueError('frame out of range')
    gold,teal=GENRE_COLORS[genre]
    canvas=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0))
    glow=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    d=ImageDraw.Draw(canvas)
    x0,y,x1=geometry.underline
    if 4<=idx<=40:
        progress=ease((idx-4)/19)
        end=x0+round((x1-x0)*progress)
        fade=1.0 if idx<32 else max(0,(41-idx)/9)
        if end>x0:
            gd.rounded_rectangle((x0,y-5,end,y+8),radius=6,fill=rgba(gold,int(75*fade)))
            d.rounded_rectangle((x0,y-2,end,y+3),radius=3,fill=rgba(gold,int(220*fade)))
            if 7<=idx<=28:
                r=6+int(3*math.sin(idx*.32)**2)
                d.ellipse((end-r,y-r,end+r,y+r),fill=rgba('#FFF0BE',int(200*fade)))
    if 20<=idx<=40:
        cx,cy=geometry.focal
        p=ease((idx-20)/10)
        fade=1.0 if idx<32 else max(0,(41-idx)/9)
        r=51+round(13*p)
        gd.ellipse((cx-r-8,cy-r-8,cx+r+8,cy+r+8),outline=rgba(teal,int(105*fade)),width=11)
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=rgba(teal,int(170*fade)),width=3)
    if idx<4: return canvas
    glow=glow.filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(glow,canvas)

def make_overlays(folder: Path, genre='ai', geometry=HookGeometry()):
    validate(geometry,genre)
    folder.mkdir(parents=True,exist_ok=True)
    for i in range(geometry.frame_count):
        draw_frame(i,genre,geometry).save(folder/f'hook_{i:03d}.png',optimize=True)

def render(source: Path, output: Path, overlays: Path, genre='ai'):
    make_overlays(overlays,genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(source),'-framerate',str(FPS),'-i',str(overlays/'hook_%03d.png'),
         '-filter_complex','[0:v][1:v]overlay=eof_action=pass:shortest=0:format=auto,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map','0:d?',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-c:d','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--overlays',type=Path,required=True)
    p.add_argument('--genre',choices=tuple(GENRE_COLORS),default='ai')
    a=p.parse_args()
    render(a.source,a.output,a.overlays,a.genre)
