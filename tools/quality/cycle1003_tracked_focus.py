"""Offline review-only 10-genre focus tracking for image-first TikTok slides.

Tracks the active cyan tab in scene02 and adds a subtle rounded focus ring.
Never modifies burned-in subtitles; Japanese AAC is stream-copied.
No posting, merging, external assets, or paid services.
"""
from pathlib import Path
import math
import subprocess
import cv2
import numpy as np

SIZE=(1080,1920)
FPS=30
ROI=(60,535,800,650)
CAPTION_TOP=1188
GENRES={
 'ai_work':(208,221,42),'business':(232,188,76),'finance':(169,219,72),
 'education':(255,183,102),'health':(182,221,86),'travel':(118,189,246),
 'cooking':(123,171,255),'lifestyle':(244,168,232),
 'technology':(240,224,78),'entertainment':(195,159,255),
}

def detect_active_tab(frame):
    x0,y0,x1,y1=ROI
    if frame.ndim!=3 or frame.shape[0]<y1 or frame.shape[1]<x1:
        raise ValueError("frame too small")
    hsv=cv2.cvtColor(frame[y0:y1,x0:x1],cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,np.array([80,90,110]),np.array([105,255,255]))
    _,_,stats,_=cv2.connectedComponentsWithStats(mask,8)
    options=[]
    for x,y,w,h,area in stats[1:]:
        if area>3300 and w>120 and 25<h<80:
            options.append((int(x+x0),int(y+y0),int(w),int(h),int(area)))
    if not options: return None
    return max(options,key=lambda item:item[4])[:4]

def rounded(im,p0,p1,r,color,thickness):
    x0,y0=p0;x1,y1=p1
    cv2.line(im,(x0+r,y0),(x1-r,y0),color,thickness,cv2.LINE_AA)
    cv2.line(im,(x0+r,y1),(x1-r,y1),color,thickness,cv2.LINE_AA)
    cv2.line(im,(x0,y0+r),(x0,y1-r),color,thickness,cv2.LINE_AA)
    cv2.line(im,(x1,y0+r),(x1,y1-r),color,thickness,cv2.LINE_AA)
    for center,a,b in [((x0+r,y0+r),180,270),((x1-r,y0+r),270,360),
                       ((x0+r,y1-r),90,180),((x1-r,y1-r),0,90)]:
        cv2.ellipse(im,center,(r,r),0,a,b,color,thickness,cv2.LINE_AA)

def add_focus(frame,bbox,genre='ai_work',strength=.8):
    if genre not in GENRES: raise ValueError("unknown genre")
    if bbox is None: return frame
    x,y,w,h=bbox
    if y+h>=CAPTION_TOP: raise ValueError("caption overlap")
    x0,y0=max(0,x-9),max(0,y-10)
    x1,y1=min(frame.shape[1]-1,x+w+9),min(frame.shape[0]-1,y+h+10)
    px0,py0=max(0,x0-28),max(0,y0-28)
    px1,py1=min(frame.shape[1],x1+29),min(frame.shape[0],y1+29)
    patch=frame[py0:py1,px0:px1]
    glow=np.zeros_like(patch)
    rounded(glow,(x0-px0,y0-py0),(x1-px0,y1-py0),18,GENRES[genre],10)
    glow=cv2.GaussianBlur(glow,(0,0),8)
    cv2.addWeighted(patch,1.0,glow,.30*strength,0,patch)
    rounded(patch,(x0-px0,y0-py0),(x1-px0,y1-py0),18,(248,250,255),3)
    return frame

def render(source,target,genre='ai_work',start=3.0,end=5.35):
    source,target=Path(source),Path(target)
    if genre not in GENRES: raise ValueError("unknown genre")
    if not (0<=start<end): raise ValueError("invalid timing")
    if not source.is_file(): raise FileNotFoundError(source)
    if source.resolve()==target.resolve(): raise ValueError("overwrite forbidden")
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError("cannot decode source")
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    if (w,h)!=SIZE or abs(fps-FPS)>.01:
        cap.release();raise ValueError("expected 1080x1920 30fps")
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s:v',f'{w}x{h}',
         '-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264',
         '-preset','veryfast','-crf','14','-pix_fmt','yuv420p',
         '-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(target)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=tracked=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if start<=frames/FPS<=end:
                box=detect_active_tab(frame)
                if box:
                    strength=.65+.15*math.sin(2*math.pi*(frames/FPS-start)*1.3)
                    add_focus(frame,box,genre,strength)
                    tracked+=1
            p.stdin.write(frame.tobytes())
            frames+=1
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError(err[-1500:])
    except Exception:
        if not p.stdin.closed:p.stdin.close()
        p.kill();p.wait();raise
    finally:
        cap.release()
    return {'frames':frames,'tracked_frames':tracked,
            'audio':'streamcopy','publication':'NOT_APPROVED'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    a=p.parse_args()
    print(render(a.input,a.output,a.genre))
