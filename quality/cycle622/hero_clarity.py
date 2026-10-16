#!/usr/bin/env python3
"""Cycle 622: brighten dark hero panels without touching existing caption areas.
Input MP4 is a local licensed/approved asset; no auto-publish.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parent
ROI=(25,445,1055,810)
FEATHER=35
LUT=np.array([min(255,round(v+29*(1-v/255)**1.6)) for v in range(256)],dtype=np.uint8)

def mask():
    x0,y0,x1,y1=ROI
    yy,xx=np.ogrid[y0:y1,x0:x1]
    d=np.minimum.reduce(np.broadcast_arrays(xx-x0,x1-1-xx,yy-y0,y1-1-yy))
    t=np.clip(d.astype(np.float32)/FEATHER,0,1)
    return (t*t*(3-2*t))[...,None]
MASK=mask()

def enhance(frame):
    x0,y0,x1,y1=ROI
    if frame.shape[:2]!=(1920,1080): raise ValueError('Requires 1080x1920')
    out=frame.copy()
    roi=frame[y0:y1,x0:x1]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    hsv[:,:,2]=cv2.LUT(hsv[:,:,2],LUT)
    lit=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    out[y0:y1,x0:x1]=np.clip(roi.astype(np.float32)*(1-MASK)+lit.astype(np.float32)*MASK,0,255).astype(np.uint8)
    return out

def render(source,output):
    source,output=Path(source),Path(output)
    cap=cv2.VideoCapture(str(source))
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (w,h,n)!=(1080,1920,468): raise ValueError(f'Unexpected dimensions/frames: {(w,h,n)}')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','17','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(n):
            ok,f=cap.read()
            if not ok:raise RuntimeError(f'Decode stopped at frame {i}')
            p.stdin.write(enhance(f).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait():raise RuntimeError(err[-1500:])
    finally:cap.release()
    return {'output':str(output),'frames':n,'publication':'NOT_APPROVED','status':'HUMAN_REVIEW'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output),ensure_ascii=False))
