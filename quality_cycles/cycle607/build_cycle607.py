#!/usr/bin/env python3
"""cycle607: local, zero-cost clean text wipe for 1080x1920 H.264/AAC video.
Uses existing user project video; does not post or approve content.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle606_baseline.mp4'
GENRES=ROOT/'assets/genres.json'
OUTPUT=ROOT/'output/cycle607_CLEAN_TEXT_WIPE_HUMAN_REVIEW.mp4'
FIRST,LAST=243,259
SOURCE_A,SOURCE_B=242,260
W,H,TOP_H=1080,1920,815

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def get_color(genre):
    data=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
    if genre not in data:raise ValueError(f'Unknown genre {genre}')
    h=data[genre]['theme'].lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def get_frame(path,index):
    cap=cv2.VideoCapture(str(path))
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES,index)
        ok,frame=cap.read()
        if not ok:raise RuntimeError(f'Cannot decode frame {index}')
        return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    finally:cap.release()

def transition_frame(a,b,k,n,accent):
    """Narrow-seam wipe: avoid full-screen double-exposed Japanese typography."""
    if a.shape!=(TOP_H,W,3) or b.shape!=a.shape:raise ValueError('bad frame dimensions')
    t=(k+1)/n
    t=t*t*(3-2*t)
    cut=-24+(W+48)*t
    x=np.arange(W,dtype=np.float32)
    alpha=np.clip((cut-x+8)/16,0,1)[None,:,None]
    rgb=np.clip(a.astype(np.float32)*(1-alpha)+b.astype(np.float32)*alpha,0,255).astype(np.uint8)
    if 0<cut<W and k<n-1:
        edge=np.abs(x-cut)
        halo=np.maximum(0,1-edge/15)*0.14
        tint=np.array(accent,dtype=np.float32).reshape(1,1,3)
        rgb=np.clip(rgb.astype(np.float32)*(1-halo[None,:,None])+tint*halo[None,:,None],0,255).astype(np.uint8)
        rgb[:,max(0,int(cut)-1):min(W,int(cut)+2)]=np.array(accent,dtype=np.uint8)
    return rgb

def render(genre='雑学・科学',input_path=None,frames_dir=None):
    src=Path(input_path) if input_path else BASE
    frames_dir=Path(frames_dir) if frames_dir else ROOT/'output/wipe_frames'
    frames_dir.mkdir(parents=True,exist_ok=True)
    a=get_frame(src,SOURCE_A)[:TOP_H]
    b=get_frame(src,SOURCE_B)[:TOP_H]
    accent=get_color(genre)
    for i in range(FIRST,LAST+1):
        frame=transition_frame(a,b,i-FIRST,LAST-FIRST+1,accent)
        Image.fromarray(frame).save(frames_dir/f'wipe_{i:03d}.png',compress_level=4)
    return frames_dir

def run(genre='雑学・科学',input_path=None,output_path=None):
    src=Path(input_path) if input_path else BASE
    out=Path(output_path) if output_path else OUTPUT
    out.parent.mkdir(parents=True,exist_ok=True)
    frames=render(genre,src,out.parent/'wipe_frames')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
         '-framerate','30','-start_number',str(FIRST),'-i',str(frames/'wipe_%03d.png'),
         '-filter_complex',f"[1:v]format=rgba,setpts=PTS+{FIRST}/30/TB[wi];[0:v][wi]overlay=x=0:y=0:eof_action=pass:enable='between(n,{FIRST},{LAST})'[v]",
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
         '-threads','1','-pix_fmt','yuv420p','-c:a','copy','-frames:v','468',
         '-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True,timeout=240)
    return {'output':str(out),'sha256':sha256(out),'genre':genre,'modified_frames':[FIRST,LAST]}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--genre',default='雑学・科学')
    p.add_argument('--input')
    p.add_argument('--output')
    args=p.parse_args()
    print(json.dumps(run(args.genre,args.input,args.output),ensure_ascii=False))
