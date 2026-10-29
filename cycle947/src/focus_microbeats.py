"""Review-only, reusable content-area microbeat camera for image-first shorts.

Does not create/modify subtitles or audio. Input MP4 must already be reviewed;
never use this as a publication or approval gate. Offline OpenCV + ffmpeg.
"""
from __future__ import annotations
import argparse
import math
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRE_PROFILES = {
    'ai_work': 1.055, 'finance': 1.045, 'business': 1.050,
    'education': 1.050, 'lifestyle': 1.045, 'health': 1.040,
    'travel': 1.055, 'food': 1.045, 'technology': 1.055,
    'career': 1.050,
}
SCENE_BOUNDARIES = (0.0, 2.9, 5.8, 8.7, 11.6, 14.5, 17.4, 20.3, 23.033333)
# Top-anchored targets keep headline and first data row visible during push-in.
SCENE_TARGETS = ((.50,.0),(.50,.0),(.50,.0),(.50,.0),(.50,.0),(.50,.0),(.50,.0),(.50,.0))
# Only center illustration area: top header, lower burned-in Japanese subtitles,
# voice-reactive meter, and footer are not edited in source pixels.
CONTENT_RECT = (20, 155, 1060, 1440)

def smoothstep(v: float) -> float:
    v = max(0., min(1., v))
    return v*v*(3-2*v)

def beat_scale(time_s: float, scene_start: float, scene_end: float, max_scale: float) -> float:
    """One slow, purposeful second-camera emphasis per scene, no sharp jumps."""
    progress = (time_s-scene_start)/(scene_end-scene_start)
    # 1st half original shot, 2nd half subtly pushed in; 200ms transition.
    return 1.0 + (max_scale-1.0)*smoothstep((progress-0.46)/0.13)

def focus_content(frame: np.ndarray, scale: float, target=(.5,.5), rect=CONTENT_RECT) -> np.ndarray:
    if frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError('expected 3-channel frame')
    if not (1.0 <= scale <= 1.10):
        raise ValueError('unsafe scale')
    x0,y0,x1,y1 = rect
    if not (0 <= x0 < x1 <= frame.shape[1] and 0 <= y0 < y1 <= frame.shape[0]):
        raise ValueError('invalid content rect')
    if not all(0 <= p <= 1 for p in target):
        raise ValueError('invalid target')
    if scale == 1.0:
        return frame.copy()
    region = frame[y0:y1, x0:x1]
    h,w=region.shape[:2]
    cw=max(2,round(w/scale)); ch=max(2,round(h/scale))
    cx=int(round(target[0]*w)); cy=int(round(target[1]*h))
    left=max(0,min(w-cw,cx-cw//2)); top=max(0,min(h-ch,cy-ch//2))
    crop=region[top:top+ch,left:left+cw]
    out=frame.copy()
    out[y0:y1,x0:x1]=cv2.resize(crop,(w,h),interpolation=cv2.INTER_LINEAR)
    return out

def scene_index(t:float)->int:
    return max(0,min(len(SCENE_TARGETS)-1,int(np.searchsorted(SCENE_BOUNDARIES,t,side='right')-1)))

def render(source:Path,dest:Path,genre:str='ai_work') -> dict:
    if genre not in GENRE_PROFILES: raise ValueError('unknown genre')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('could not open source')
    fps=cap.get(cv2.CAP_PROP_FPS); w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (w,h)!=(1080,1920) or abs(fps-30)>0.01 or n!=691:
        cap.release(); raise RuntimeError(f'fail closed on unexpected source: {w}x{h} {fps}fps {n} frames')
    dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size',f'{w}x{h}','-framerate','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dest)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for i in range(n):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'source decode stopped at frame {i}')
            t=i/fps; s=scene_index(t)
            scale=beat_scale(t,SCENE_BOUNDARIES[s],SCENE_BOUNDARIES[s+1],GENRE_PROFILES[genre])
            if scale>1.0001: changed+=1
            out=focus_content(frame,scale,SCENE_TARGETS[s])
            proc.stdin.write(out.tobytes())
        proc.stdin.close(); err=proc.stderr.read().decode('utf-8','replace'); code=proc.wait()
        if code: raise RuntimeError(f'ffmpeg failed {code}: {err[-2000:]}')
    except Exception:
        proc.kill(); proc.wait(); raise
    finally: cap.release()
    return {'frames':n,'fps':fps,'resolution':[w,h],'changed_frames':changed,'genre':genre,'audio':'stream-copy','publication_approved':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--output',required=True);parser.add_argument('--genre',default='ai_work');a=parser.parse_args()
    print(render(Path(a.source),Path(a.output),a.genre))
