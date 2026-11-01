#!/usr/bin/env python3
"""Offline, genre-agnostic numeric proof trace for a captioned vertical video.

This is a *fictional* spreadsheet demonstration. It does not claim to run Excel.
Only pixels in a declared story-area window change; Japanese narration and
subtitles are copied unchanged. No external assets, posting, or network calls.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
FPS, WIDTH, HEIGHT = 30, 1080, 1920
CAPTION_TOP = 1160

@dataclass(frozen=True)
class Proof:
    values: tuple[int, ...]
    result: int
    cells: tuple[tuple[int,int,int,int], ...]
    result_cell: tuple[int,int,int,int]
    first_frame: int
    last_frame: int
    status_box: tuple[int,int,int,int]
    caption_top: int = CAPTION_TOP

DEMO = Proof(
    values=(9,14,21), result=44,
    cells=((469,817,636,862),(469,863,636,915),(469,916,636,969)),
    result_cell=(469,971,636,1044),
    first_frame=181,last_frame=218,
    status_box=(90,1060,839,1151),
)

def validate(p: Proof, frame_count: int):
    if not p.values or len(p.values)!=len(p.cells): raise ValueError('cells/values mismatch')
    if sum(p.values)!=p.result: raise ValueError('fictional arithmetic inconsistent')
    if any(not isinstance(v,int) or v<0 for v in p.values): raise ValueError('invalid numbers')
    if not (0<=p.first_frame<p.last_frame<=frame_count): raise ValueError('invalid frame window')
    if p.last_frame-p.first_frame<4*(len(p.values)+1): raise ValueError('insufficient timing')
    if not (800<=p.caption_top<=HEIGHT-200): raise ValueError('caption protection invalid')
    for box in (*p.cells,p.result_cell,p.status_box):
        x0,y0,x1,y1=box
        if not (0<=x0<x1<=WIDTH and 0<=y0<y1<p.caption_top):
            raise ValueError('box overlaps subtitle or outside frame')
    return True

def phase_for(frame: int, p: Proof):
    if not p.first_frame<=frame<p.last_frame: return None
    stages=len(p.values)+1
    stage=min(stages-1,(frame-p.first_frame)*stages//(p.last_frame-p.first_frame))
    stage_start=p.first_frame+stage*(p.last_frame-p.first_frame)//stages
    opacity=min(1.0,max(0.0,(frame-stage_start+1)/5.0))
    return stage,opacity

def font_path():
    import os
    path=os.getenv('TIKTOK_JP_FONT')
    if path and Path(path).is_file():return path
    try:
        p=subprocess.check_output(['fc-match','-f','%{file}','Noto Sans CJK JP'],text=True).strip()
        if p and Path(p).is_file():return p
    except (OSError,subprocess.CalledProcessError):pass
    raise RuntimeError('Noto Sans CJK JP font unavailable; install fonts-noto-cjk')

def annotate(frame: np.ndarray, idx: int, p: Proof, font_file: str):
    """Return frame with evidence-focused cell trace; source remains untouched."""
    validate(p, max(idx+1,p.last_frame))
    state=phase_for(idx,p)
    if state is None:return frame.copy()
    stage,opacity=state
    out=frame.copy()
    target=p.cells[stage] if stage<len(p.values) else p.result_cell
    x0,y0,x1,y1=target
    # Bounded teal halo around one cell at a time; never touches subtitles.
    padding=15
    xa,ya,xb,yb=max(0,x0-padding),max(0,y0-padding),min(WIDTH,x1+padding),min(p.caption_top,y1+padding)
    halo=np.zeros((yb-ya,xb-xa,3),dtype=np.uint8)
    cv2.rectangle(halo,(x0-xa,y0-ya),(x1-xa,y1-ya),(225,237,72),6)
    halo=cv2.GaussianBlur(halo,(0,0),6)
    roi=out[ya:yb,xa:xb]
    cv2.addWeighted(roi,1.0,halo,0.75*opacity,0,dst=roi)
    cv2.rectangle(out,(x0,y0),(x1,y1),(225,237,72),max(1,round(4*opacity)))
    # Replace only the spreadsheet's fictional status line with a verifiable sum.
    rgb=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB))
    layer=Image.new('RGBA',rgb.size,(0,0,0,0));draw=ImageDraw.Draw(layer)
    sx0,sy0,sx1,sy1=p.status_box
    draw.rounded_rectangle((sx0,sy0,sx1,sy1),radius=15,
                           fill=(3,30,43,int(248*opacity)),outline=(83,224,202,int(210*opacity)),width=2)
    small=ImageFont.truetype(font_file,25)
    big=ImageFont.truetype(font_file,40)
    text=' + '.join(str(v) for v in p.values[:min(stage+1,len(p.values))])
    if stage==len(p.values):text+=f' = {p.result}'
    draw.text((sx0+18,sy0+22),'計算の確認',font=small,fill=(161,230,220,int(255*opacity)))
    draw.text((sx0+190,sy0+13),text,font=big,fill=(250,255,255,int(255*opacity)))
    rgb=Image.alpha_composite(rgb.convert('RGBA'),layer).convert('RGB')
    out=cv2.cvtColor(np.asarray(rgb),cv2.COLOR_RGB2BGR)
    return out

def render(source: str, dest: str, proof: Proof=DEMO, genre: str='ai'):
    if genre not in GENRES:raise ValueError('unknown genre')
    source,dest=Path(source),Path(dest)
    if not source.is_file():raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('cannot read source')
    width,height=int(cap.get(3)),int(cap.get(4))
    fps=cap.get(cv2.CAP_PROP_FPS);frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (width,height)!=(WIDTH,HEIGHT) or abs(fps-FPS)>0.01:raise ValueError('source must be 1080x1920 30fps')
    validate(proof,frames)
    font_file=font_path();dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dest)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    i=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if proof.first_frame<=i<proof.last_frame:
                frame=annotate(frame,i,proof,font_file)
            proc.stdin.write(frame.tobytes());i+=1
        proc.stdin.close();error=proc.stderr.read();code=proc.wait()
        if code:raise RuntimeError(error.decode(errors='replace')[-2000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed:proc.stdin.close()
        proc.kill();proc.wait();raise
    finally:cap.release()
    if i!=frames:raise RuntimeError(f'frame count mismatch: {i} != {frames}')
    return {'frames':i,'proof_sum':proof.result,'active_frames':proof.last_frame-proof.first_frame,
            'genres_supported':len(GENRES),'genre_rendered':genre}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output')
    ap.add_argument('--genre',choices=GENRES,default='ai')
    a=ap.parse_args();print(render(a.source,a.output,genre=a.genre))
