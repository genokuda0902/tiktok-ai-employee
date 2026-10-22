#!/usr/bin/env python3
"""Cycle769: genre-neutral scene-cut micro-dissolves, preserving voice/subtitle areas.
No external APIs, stock media, or paid services.
"""
from __future__ import annotations
import argparse, subprocess, sys, os
import cv2
import numpy as np

W,H,FPS,N = 1080,1920,30,429
# Cuts determined by source-video image discontinuities, not by guessed narration.
CUTS=(61,120,379)
BLEND_FRAMES=5
# Replace source's near-black wipe artifacts using clean neighboring slides.
# tuple: [first_bad, first_clean_after, last_clean_before, first_clean_after]
WIPES=((180,181,179,181),(237,244,236,244),(280,283,279,283),(326,330,325,330))
ART_TOP,ART_BOTTOM=240,1200  # preserve top UI and lower Japanese subtitle card

def eased_alpha(step:int, total:int=BLEND_FRAMES)->float:
    t=(step+1)/(total+1)
    return t*t*(3-2*t)

def blend_art(previous:np.ndarray, current:np.ndarray, step:int)->np.ndarray:
    if previous.shape != (H,W,3) or current.shape != (H,W,3):
        raise ValueError("Expected 1080x1920 BGR")
    alpha=eased_alpha(step)
    out=current.copy()
    out[ART_TOP:ART_BOTTOM]=cv2.addWeighted(
        previous[ART_TOP:ART_BOTTOM],1-alpha,
        current[ART_TOP:ART_BOTTOM],alpha,0)
    return out

def clean_wipe(old:np.ndarray,new:np.ndarray,progress:float,edge_px:int=54)->np.ndarray:
    """Replace black wipe with two complete slides and a feathered moving seam."""
    if old.shape != (H,W,3) or new.shape != (H,W,3):
        raise ValueError("Expected 1080x1920 BGR")
    boundary=W*(1-progress)
    x=np.arange(W,dtype=np.float32)
    alpha=np.clip((boundary-x)/edge_px+0.5,0,1)
    # Blend only the narrow seam; keep all other pixels exactly from a clean slide.
    out=old.copy()
    right_edge=int(max(0,min(W,boundary-edge_px/2)))
    left_edge=int(max(0,min(W,boundary+edge_px/2)))
    out[:,:right_edge]=new[:,:right_edge]
    if left_edge>right_edge:
        a=alpha[right_edge:left_edge].reshape(1,-1,1)
        out[:,right_edge:left_edge]=(new[:,right_edge:left_edge]*a+
                                    old[:,right_edge:left_edge]*(1-a)).astype(np.uint8)
    return out

def render(src:str,dst:str):
    cap=cv2.VideoCapture(src)
    if (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))!=(W,H,N):
        raise ValueError("Source must have 429 frames at 1080x1920")
    if abs(cap.get(cv2.CAP_PROP_FPS)-FPS)>.01:raise ValueError("Source must be 30fps")
    tmp=dst+'.video_tmp.mp4'
    cmd=['ffmpeg','-y','-nostdin','-hide_banner','-loglevel','error',
         '-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}',
         '-framerate',str(FPS),'-i','pipe:0','-i',src,
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast',
         '-crf','20','-threads','4','-pix_fmt','yuv420p','-r',str(FPS),
         '-frames:v',str(N),'-an','-movflags','+faststart',tmp]
    # Cache clean source frames before streaming; avoids decoding lookahead in the hot loop.
    stable={}
    for _,_,left,right in WIPES:
        for k in (left,right):
            if k not in stable:
                cap.set(cv2.CAP_PROP_POS_FRAMES,k)
                ok,fr=cap.read()
                if not ok:raise RuntimeError(f'Cannot read anchor {k}')
                stable[k]=fr
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    anchor=None
    try:
        for i in range(N):
            ok,frame=cap.read()
            if not ok:raise RuntimeError(f'Input truncated at {i}')
            if i+1 in CUTS:anchor=frame.copy()
            for start,end,left,right in WIPES:
                if start<=i<end:
                    t=(i-start+1)/(end-start+1)
                    frame=clean_wipe(stable[left],stable[right],t)
                    break
            else:
                for b in CUTS:
                    if b<=i<b+BLEND_FRAMES:
                        if anchor is None:raise RuntimeError('Missing previous scene anchor')
                        frame=blend_art(anchor,frame,i-b)
                        break
            p.stdin.write(frame.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        ret=p.wait()
        if ret:raise RuntimeError(f'FFmpeg exit {ret}: {err[-1200:]}')
        mux=['ffmpeg','-y','-nostdin','-loglevel','error','-i',tmp,'-i',src,
             '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',dst]
        subprocess.run(mux,check=True,capture_output=True)
        os.remove(tmp)
    except Exception:
        if p.stdin and not p.stdin.closed:p.stdin.close()
        p.kill();p.wait()
        raise
    finally:
        cap.release()
    return dst

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--input',required=True)
    a.add_argument('--output',required=True)
    x=a.parse_args()
    print(render(x.input,x.output))
