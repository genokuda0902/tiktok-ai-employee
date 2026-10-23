#!/usr/bin/env python3
"""Artwork-only matte dip transition. Requires a licensed, reviewed source MP4.
No external TTS, no paid APIs, no posting. Audio packets are copied unchanged.
"""
import argparse, math, subprocess
from pathlib import Path
import cv2
import numpy as np

GENRE_THEMES = {
    "ai_work":"#9B90FF","beauty":"#E5ACD7",
    "love_psychology":"#C0A2FF","money_saving":"#6BE1B8",
    "sales_business":"#58C5F6","career":"#83C5F9",
    "health_life":"#6EE7BE","science":"#39E7D3",
    "travel_food":"#70D6EA","product_life":"#C6A0F5"
}
DEFAULT_SCENE_FRAMES=(57,63,58,63,40,47,48,53)
ART_RECT=(90,560,900,620)

def transition_weight(index,boundary,half_window=5):
    distance=abs(index+0.5-boundary)
    if distance>=half_window:return 0.
    return math.cos(math.pi*distance/(2*half_window))**2

def matte_transition(frame,weight,rect=ART_RECT,matte_rgb=(13,38,58)):
    if weight<=0:return frame
    h,w=frame.shape[:2]
    x,y,rw,rh=(int(round(a*s)) for a,s in zip(
        rect,(w/1080,h/1920,w/1080,h/1920)))
    x,y=max(0,x),max(0,y)
    rw,rh=min(rw,w-x),min(rh,h-y)
    if rw<=0 or rh<=0:return frame
    feather=max(1,int(round(48*min(w/1080,h/1920))))
    xx=np.minimum(np.arange(rw),np.arange(rw)[::-1])
    yy=np.minimum(np.arange(rh),np.arange(rh)[::-1])
    edge=np.minimum(yy[:,None],xx[None,:]).astype(np.float32)
    mask=np.clip(edge/feather,0,1)
    mask=mask*mask*(3-2*mask)
    alpha=(.995*weight*mask)[:,:,None]
    roi=frame[y:y+rh,x:x+rw]
    out=frame.copy()
    out[y:y+rh,x:x+rw]=np.clip(
        roi.astype(np.float32)*(1-alpha)
        +np.array(matte_rgb[::-1],dtype=np.float32)*alpha,0,255
    ).astype(np.uint8)
    return out

def process_frame(frame,index,scene_frames=DEFAULT_SCENE_FRAMES,half_window=5):
    boundary=0
    for count in scene_frames[:-1]:
        boundary+=count
        weight=transition_weight(index,boundary,half_window)
        if weight>0:return matte_transition(frame,weight)
    return frame

def render(source,target,scene_frames=DEFAULT_SCENE_FRAMES):
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError("Input MP4 unavailable")
    w,h=int(cap.get(3)),int(cap.get(4))
    fps=cap.get(cv2.CAP_PROP_FPS)
    if (w,h)!=(1080,1920) or abs(fps-30)>.1:
        raise ValueError(f"Expected 1080x1920 30fps, got {w}x{h} {fps}")
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",
        "-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}",
        "-r","30","-i","pipe:0","-i",str(source),
        "-map","0:v:0","-map","1:a:0",
        "-c:v","libx264","-preset","ultrafast","-crf","18",
        "-pix_fmt","yuv420p","-c:a","copy",
        "-movflags","+faststart",str(target)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            p.stdin.write(process_frame(frame,count,scene_frames).tobytes())
            count+=1
    except Exception:
        p.kill()
        raise
    finally:
        cap.release()
        if p.stdin:p.stdin.close()
    err=p.stderr.read().decode("utf-8","replace")
    if p.wait()!=0:raise RuntimeError(err[-2000:])
    if count!=sum(scene_frames):
        raise ValueError(f"Unexpected frame count: {count} vs {sum(scene_frames)}")
    return target

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--frames",default=",".join(map(str,DEFAULT_SCENE_FRAMES)))
    args=p.parse_args()
    frames=tuple(int(v) for v in args.frames.split(","))
    if len(frames)<2 or any(n<12 for n in frames):
        p.error("Need two or more scenes of 12+ frames")
    print(render(args.input,args.output,frames))
