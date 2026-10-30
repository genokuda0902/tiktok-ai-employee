#!/usr/bin/env python3
"""Cycle1101: motion-safe Japanese 3-step learning rail for vertical slides.

Purpose: show three consecutive ideas without trying to track moving UI screenshots.
The compact rail occupies y1630..1724, below burned captions ending near y1620
and above the progress bar near y1745. No external assets, paid services, or posting.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import subprocess

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_END = 1625
PROGRESS_START = 1740
RAIL = (48, 1630, 984, 94)
GENRE_ACCENTS = {
    'ai_work':'0x39DDC6','trivia':'0xF0C76B','cooking':'0xF9A96C',
    'beauty':'0xF6B3C9','money':'0x7DDB99','health':'0x73D5B4',
    'travel':'0x75C9F2','product':'0xA4BBFF','story':'0xD8A9F2',
    'work_skills':'0x6CD8D6',
}

@dataclass(frozen=True)
class Stage:
    scene: int
    index: int
    first: int
    last: int

CHAPTERS = {4:(258,339,('目的','条件','形式')),5:(340,422,('数字・根拠','日付・名前','断定表現'))}
STAGES = (
    Stage(4,1,260,286),Stage(4,2,288,314),Stage(4,3,316,338),
    Stage(5,1,342,368),Stage(5,2,370,396),Stage(5,3,398,421),
)

def validate(stages=STAGES,rail=RAIL,width=WIDTH,height=HEIGHT):
    if (width,height)!=(WIDTH,HEIGHT):raise ValueError('Expected 1080x1920 template')
    x,y,w,h=rail
    if x<0 or x+w>width or y<CAPTION_END or y+h>=PROGRESS_START:
        raise ValueError('Learning rail overlaps subtitles or progress bar')
    if not stages:raise ValueError('No stages')
    prev=-1;by_scene={}
    for s in stages:
        if s.scene not in CHAPTERS:raise ValueError('Unknown chapter')
        start,end,_=CHAPTERS[s.scene]
        if not(start<=s.first<=s.last<=end) or s.first<=prev:
            raise ValueError('Invalid/overlapping timing')
        if s.index not in (1,2,3):raise ValueError('Index outside 1..3')
        by_scene.setdefault(s.scene,[]).append(s.index)
        prev=s.last
    if any(v != [1,2,3] for v in by_scene.values()):
        raise ValueError('Each chapter needs three ordered stages')
    return True

def cjk_font():
    for p in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
              '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'):
        if Path(p).is_file():return p
    p=subprocess.check_output(['fc-match','-f','%{file}','sans:lang=ja'],text=True).strip()
    if not Path(p).is_file():raise FileNotFoundError('Install fonts-noto-cjk')
    return p

def filtergraph(genre='ai_work',stages=STAGES,fontfile=None):
    validate(stages)
    if genre not in GENRE_ACCENTS:raise ValueError('Unknown genre')
    fontfile=fontfile or cjk_font()
    if not Path(fontfile).is_file():raise FileNotFoundError(fontfile)
    fontfile=fontfile.replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
    accent=GENRE_ACCENTS[genre]
    f=[]
    for scene,(start,end,labels) in CHAPTERS.items():
        en=f'between(n,{start},{end})'
        f.append(f"drawbox=x=48:y=1630:w=984:h=94:color=0x08182A@0.96:t=fill:enable='{en}'")
        f.append(f"drawbox=x=48:y=1630:w=984:h=94:color={accent}@0.72:t=2:enable='{en}'")
        for i,label in enumerate(labels):
            x=76+326*i
            f.append(f"drawbox=x={x}:y=1641:w=278:h=70:color=0x18324A@1:t=fill:enable='{en}'")
            f.append(f"drawbox=x={x}:y=1641:w=278:h=70:color=0x45687A@0.9:t=2:enable='{en}'")
            f.append(f"drawtext=fontfile='{fontfile}':text='{i+1:02d}':fontcolor=0x83A4B4:fontsize=23:x={x+12}:y=1660:enable='{en}'")
            f.append(f"drawtext=fontfile='{fontfile}':text='{label}':fontcolor=0xE1ECF0:fontsize=31:x={x+53}:y=1656:enable='{en}'")
    for s in stages:
        en=f'between(n,{s.first},{s.last})'
        x=76+326*(s.index-1)
        f.append(f"drawbox=x={x}:y=1641:w=278:h=70:color={accent}@0.18:t=fill:enable='{en}'")
        f.append(f"drawbox=x={x}:y=1641:w=278:h=70:color={accent}@1:t=5:enable='{en}'")
        f.append(f"drawbox=x={x+10}:y=1704:w=258:h=5:color={accent}@1:t=fill:enable='{en}'")
    f.append('format=yuv420p')
    return ','.join(f)

def render(source,destination,genre='ai_work',preset='veryfast',crf=20):
    source=Path(source);destination=Path(destination)
    if not source.is_file():raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-vf',filtergraph(genre),'-map','0:v:0','-map','0:a:0','-map','0:d?',
         '-map_metadata','0','-map_chapters','0','-c:v','libx264','-preset',preset,
         '-crf',str(crf),'-pix_fmt','yuv420p','-c:a','copy','-c:d','copy',
         '-movflags','+faststart',str(destination)]
    subprocess.run(cmd,check=True)
    return destination

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('source');ap.add_argument('destination')
    ap.add_argument('--genre',choices=GENRE_ACCENTS.keys(),default='ai_work')
    ap.add_argument('--preset',default='veryfast');ap.add_argument('--crf',type=int,default=20)
    a=ap.parse_args();render(a.source,a.destination,a.genre,a.preset,a.crf)
