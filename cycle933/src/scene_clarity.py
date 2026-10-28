"""Edge-aware Japanese text clarity pass. No posting, network or paid assets.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import cv2
import numpy as np

FPS=30
SIZE=(1080,1920)
SCENE_START=5.8
SCENE_END=8.7
CONTENT_BOUNDS=(105,365,810,1080)
GENRE_PROFILES={
    'ai_productivity':0.48,'business':0.43,'finance':0.45,
    'education':0.46,'health':0.38,'beauty':0.36,
    'food':0.38,'travel':0.40,'lifestyle':0.39,'technology':0.48,
}

def smoothstep(x):
    x=max(0.0,min(1.0,x))
    return x*x*(3-2*x)

def strength_at(t,genre='ai_productivity'):
    if genre not in GENRE_PROFILES:
        raise ValueError('Unknown genre: fail closed')
    if not (SCENE_START<=t<SCENE_END):
        return 0.0
    return GENRE_PROFILES[genre]*smoothstep((t-SCENE_START)/0.6)

def feather_mask(w,h,feather=32):
    xx=np.minimum(np.arange(w),w-1-np.arange(w))
    yy=np.minimum(np.arange(h),h-1-np.arange(h))
    return (np.clip(xx/feather,0,1)[None,:]*np.clip(yy/feather,0,1)[:,None]).astype(np.float32)[:,:,None]

def render_frame(frame,t,genre='ai_productivity',mask=None):
    if frame.shape!=(SIZE[1],SIZE[0],3):
        raise ValueError('Expected BGR 1080x1920 frame')
    strength=strength_at(t,genre)
    if strength==0:
        return frame.copy()
    x0,y0,x1,y1=CONTENT_BOUNDS
    roi=frame[y0:y1,x0:x1]
    blurred=cv2.GaussianBlur(roi,(0,0),1.15)
    sharpened=cv2.addWeighted(roi,1.0+strength,blurred,-strength,0)
    edge=cv2.cvtColor(cv2.absdiff(roi,blurred),cv2.COLOR_BGR2GRAY).astype(np.float32)
    edge_weight=np.clip(edge/4.0,0,1)[:,:,None]
    spatial=feather_mask(x1-x0,y1-y0) if mask is None else mask
    alpha=spatial*edge_weight
    out=frame.copy()
    out[y0:y1,x0:x1]=np.clip(sharpened.astype(np.float32)*alpha+roi.astype(np.float32)*(1-alpha),0,255).astype(np.uint8)
    return out

def produce(source:Path,target:Path,genre='ai_productivity'):
    if genre not in GENRE_PROFILES:
        raise ValueError('Unknown genre')
    if not source.is_file():
        raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError('Could not decode source')
    w,h=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    if (w,h)!=SIZE or abs(fps-FPS)>0.01:
        raise ValueError('Source format mismatch')
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
         '-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(target)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    x0,y0,x1,y1=CONTENT_BOUNDS
    mask=feather_mask(x1-x0,y1-y0)
    count=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:
                break
            t=count/FPS
            if SCENE_START<=t<SCENE_END:
                frame=render_frame(frame,t,genre,mask)
            proc.stdin.write(frame.tobytes())
            count+=1
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8','replace')
        code=proc.wait()
        if code:
            raise RuntimeError(f'ffmpeg failed {code}: {err[-1500:]}')
    finally:
        cap.release()
        if proc.poll() is None:
            proc.kill()
    return count

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=list(GENRE_PROFILES),default='ai_productivity')
    a=p.parse_args()
    print('frames:',produce(a.source,a.output,a.genre))
