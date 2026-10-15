#!/usr/bin/env python3
"""Cycle609: zero-cost hero-panel legibility, keeping captions and audio unchanged."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle608_baseline.mp4'
OUTPUT=ROOT/'output/cycle609_HERO_LEGIBILITY_HUMAN_REVIEW.mp4'
GENRES=ROOT/'assets/genres.json'
REGION=(0,220,1080,595)
def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    return h.hexdigest()
def validate_genre(genre):
    genres=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
    if genre not in genres:raise ValueError(f'Unsupported genre: {genre}')
    return genres[genre]
def video_filter():
    x,y,width,height=REGION
    return (f'[0:v]split[base][hero];'
            f'[hero]crop={width}:{height}:{x}:{y},'
            'eq=contrast=1.13:brightness=0.018:saturation=1.06,'
            'unsharp=5:5:0.60:5:5:0[enhanced];'
            f'[base][enhanced]overlay={x}:{y}:format=auto[v]')
def render(genre='雑学・科学',source=BASE,output=OUTPUT):
    validate_genre(genre)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',video_filter(),'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-threads','1',
         '-pix_fmt','yuv420p','-r','30','-c:a','copy','-frames:v','468',
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=260)
    return {'path':str(output),'sha256':sha256(output),'region':REGION,
            'genre':genre,'review':'HUMAN_REVIEW','publication':'NOT_APPROVED'}
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--genre',default='雑学・科学')
    parser.add_argument('--input',type=Path,default=BASE)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    print(json.dumps(render(args.genre,args.input,args.output),ensure_ascii=False))
