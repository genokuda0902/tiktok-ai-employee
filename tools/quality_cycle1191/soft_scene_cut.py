#!/usr/bin/env python3
"""Offline, reusable 9:16 soft scene cuts; preserves Japanese audio and caption timing."""
import argparse
from pathlib import Path
import subprocess
import cv2
import numpy as np

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
DEFAULT_CUTS=(94,168,250,330,412,499,575)
WIDTH,HEIGHT,FPS=1080,1920,30

def ease(t):
    t=max(0.,min(1.,float(t)))
    return t*t*(3-2*t)

def validate(cuts,count,transition=6,caption_top=1320):
    if not 2<=transition<=12 or not 800<=caption_top<=HEIGHT-100:
        raise ValueError('invalid safe-area/transition')
    if list(cuts)!=sorted(set(cuts)):raise ValueError('cuts not sorted and unique')
    if any(c<transition or c+transition>=count for c in cuts):
        raise ValueError('cut outside frame range')
    if any(b-a<transition*3 for a,b in zip(cuts,cuts[1:])):
        raise ValueError('cuts too close')

def blend(previous,current,phase,transition=6,caption_top=1320):
    if previous.shape!=current.shape or not 0<=phase<transition:
        raise ValueError('invalid frame or phase')
    out=current.copy()
    alpha=ease((phase+1)/transition)
    out[:caption_top]=cv2.addWeighted(previous[:caption_top],1-alpha,current[:caption_top],alpha,0)
    return out

def detect(source,threshold=14,min_gap=20):
    cap=cv2.VideoCapture(str(source));last=None;cuts=[];i=0
    if not cap.isOpened():raise ValueError('cannot read video')
    while True:
        ok,frame=cap.read()
        if not ok:break
        gray=cv2.cvtColor(cv2.resize(frame,(135,240)),cv2.COLOR_BGR2GRAY)
        if last is not None and cv2.absdiff(gray,last).mean()>threshold and (not cuts or i-cuts[-1]>=min_gap):
            cuts.append(i)
        last=gray;i+=1
    cap.release()
    return cuts,i

def render(source,output,cuts=DEFAULT_CUTS,genre='ai',transition=6,caption_top=1320):
    if genre not in GENRES:raise ValueError('invalid genre')
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise ValueError('cannot open source')
    w,h=int(cap.get(3)),int(cap.get(4))
    fps=cap.get(5);count=int(cap.get(7))
    if (w,h)!=(WIDTH,HEIGHT) or abs(fps-FPS)>.01:raise ValueError('1080x1920 30fps required')
    validate(cuts,count,transition,caption_top)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{w}x{h}','-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    i=0;prev=None;outgoing=None;cut_index=0;phase=-1
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if cut_index<len(cuts) and i==cuts[cut_index]:
                outgoing=prev.copy();phase=0;cut_index+=1
            if 0<=phase<transition:
                frame_out=blend(outgoing,frame,phase,transition,caption_top);phase+=1
            else:frame_out=frame
            proc.stdin.write(frame_out.tobytes())
            prev=frame;i+=1
        proc.stdin.close()
        err=proc.stderr.read()
        if proc.wait():raise RuntimeError(err.decode(errors='replace')[-1000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed:proc.stdin.close()
        proc.kill();proc.wait();raise
    finally:cap.release()
    if i!=count:raise RuntimeError('frame count changed')
    return i

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=GENRES,default='ai')
    p.add_argument('--auto-detect',action='store_true')
    a=p.parse_args()
    cuts=detect(a.source)[0] if a.auto_detect else DEFAULT_CUTS
    print('frames:',render(a.source,a.output,cuts=cuts,genre=a.genre),'cuts:',cuts)
