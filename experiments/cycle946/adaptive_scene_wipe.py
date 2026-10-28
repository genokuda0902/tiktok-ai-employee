"""Cycle946: safe, adaptive feathered scene transitions; review-only.

The original audio is stream-copied; all frames are retained. No external
assets, uploads, automated posting, or network calls.
"""
import argparse
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES = {
 "ai_productivity":(7,120), "business":(6,110), "education":(8,140),
 "finance":(6,100), "technology":(7,120), "health":(8,160),
 "lifestyle":(8,160), "travel":(9,180), "food":(8,140),
 "entertainment":(6,110)
}

def hard_cuts(path, threshold=18, spacing=35):
    cap=cv2.VideoCapture(str(path))
    if not cap.isOpened(): raise FileNotFoundError(path)
    prev=None; candidates=[]; i=0
    while True:
        ok,f=cap.read()
        if not ok: break
        small=cv2.resize(f,(108,192),interpolation=cv2.INTER_AREA)
        if prev is not None:
            score=float(np.abs(small.astype(np.int16)-prev.astype(np.int16)).mean())
            if score>=threshold and i>=87: candidates.append((i,score))
        prev=small; i+=1
    cap.release()
    chosen=[]
    for item in sorted(candidates,key=lambda x:-x[1]):
        if all(abs(item[0]-x[0])>=spacing for x in chosen): chosen.append(item)
    return sorted(chosen)

def wipe(old,new,beat,total,feather,direction=1,protect_chrome=True):
    if old.shape!=new.shape or old.dtype!=np.uint8: raise ValueError("invalid frames")
    if total<2 or not 0<=beat<total or not 0<feather<=new.shape[1]:
        raise ValueError("invalid transition")
    h,w=new.shape[:2]
    x=np.arange(w,dtype=np.float32)
    if direction<0: x=w-1-x
    center=-feather/2+(beat+1)/total*(w+feather)
    alpha=np.clip((center-x)/feather+.5,0,1)
    alpha=alpha*alpha*(3-2*alpha)
    if protect_chrome:
        y=np.arange(h,dtype=np.float32)
        top,bottom,ramp=round(h*.18),round(h*.74),max(1,round(h*.025))
        region=np.minimum(np.clip((y-top)/ramp,0,1),
                          np.clip((bottom-y)/ramp,0,1))
        alpha=1-region[:,None]*(1-alpha[None,:])
    else: alpha=alpha[None,:]
    return np.clip(old.astype(np.float32)*(1-alpha[:,:,None])+
                   new.astype(np.float32)*alpha[:,:,None],0,255).astype(np.uint8)

def render(source,output,genre="ai_productivity",threshold=18,max_cuts=3):
    if genre not in GENRES: raise ValueError("unknown genre")
    duration,feather=GENRES[genre]
    cuts=hard_cuts(source,threshold)[:max_cuts]
    cap=cv2.VideoCapture(str(source))
    fps=cap.get(cv2.CAP_PROP_FPS)
    w,h=int(cap.get(3)),int(cap.get(4))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    command=["ffmpeg","-hide_banner","-loglevel","error","-y",
      "-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}",
      "-r",str(fps),"-i","pipe:0","-i",str(source),
      "-map","0:v:0","-map","1:a:0","-c:v","libx264",
      "-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
      "-c:a","copy","-movflags","+faststart",str(output)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    cutmap={frame:j for j,(frame,_) in enumerate(cuts)}
    prev=None;active=None
    try:
        for i in range(count):
            ok,f=cap.read()
            if not ok: raise RuntimeError(f"decode stopped at {i}/{count}")
            if i in cutmap:
                active=(i,prev.copy(),1 if cutmap[i]%2==0 else -1)
            if active is not None:
                start,old,direction=active
                if i<start+duration:
                    f=wipe(old,f,i-start,duration,feather,direction)
                else: active=None
            proc.stdin.write(f.tobytes())
            prev=f
        proc.stdin.close()
        err=proc.stderr.read().decode("utf8","replace")
        if proc.wait()!=0: raise RuntimeError(err[-1000:])
    finally:
        cap.release()
        if proc.poll() is None: proc.kill()
    return {"frames":count,"fps":fps,"resolution":[w,h],"cuts":cuts,
            "genre":genre,"duration_frames":duration,"feather_px":feather,
            "publication":"HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("output")
    p.add_argument("--genre",choices=GENRES,default="ai_productivity")
    p.add_argument("--report")
    a=p.parse_args()
    result=render(a.source,a.output,a.genre)
    if a.report: Path(a.report).write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
