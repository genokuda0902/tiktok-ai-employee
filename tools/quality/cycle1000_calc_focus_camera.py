#!/usr/bin/env python3
"""Review-only guided push-in for spreadsheet scenes, with no new external assets."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
ROI = (40,335,1000,720)
KEYFRAMES = ((6.35,1.0,.50,.40),(6.78,1.16,.55,.37),
             (7.24,1.16,.55,.37),(7.55,1.16,.54,.68),
             (8.12,1.16,.54,.68),(8.50,1.0,.50,.50))

def run(cmd):
    return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def smooth(t):
    t=np.clip(t,0.0,1.0)
    return float(t*t*(3-2*t))

def camera_at(t,keyframes=KEYFRAMES):
    if t<keyframes[0][0] or t>keyframes[-1][0]: return (1.,.5,.5)
    for i in range(len(keyframes)-1):
        a,b=keyframes[i],keyframes[i+1]
        if a[0]<=t<=b[0]:
            w=smooth((t-a[0])/(b[0]-a[0]))
            return tuple(float(a[j]*(1-w)+b[j]*w) for j in (1,2,3))
    return (1.,.5,.5)

def focus_frame(frame,t,roi=ROI):
    z,cx,cy=camera_at(t)
    if z<=1.0001: return frame
    x,y,w,h=roi
    if x<0 or y<0 or x+w>frame.shape[1] or y+h>frame.shape[0]:
        raise ValueError('invalid safe ROI')
    crop=frame[y:y+h,x:x+w]
    cw=int(round(w/z));ch=int(round(h/z))
    left=int(round(cx*w-cw/2));top=int(round(cy*h-ch/2))
    left=max(0,min(w-cw,left));top=max(0,min(h-ch,top))
    zoomed=cv2.resize(crop[top:top+ch,left:left+cw],(w,h),interpolation=cv2.INTER_LINEAR)
    out=frame.copy()
    feather=20
    mx=np.minimum(np.arange(w),np.arange(w)[::-1])/feather
    my=np.minimum(np.arange(h),np.arange(h)[::-1])/feather
    alpha=np.minimum(1,np.minimum(mx[None,:],my[:,None]))[:,:,None].astype('float32')
    out[y:y+h,x:x+w]=np.rint(crop.astype('float32')*(1-alpha)+zoomed.astype('float32')*alpha).astype('uint8')
    return out

def render(source,output,report,genre,review_only):
    source=Path(source);output=Path(output);report=Path(report)
    if not review_only or genre not in GENRES: raise ValueError('review-only 10-genre gate')
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('source/output invalid')
    p=probe(source)
    video=next((s for s in p['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
    subtitle=next((s for s in p['streams'] if s['codec_type']=='subtitle'),None)
    if not video or (video['width'],video['height'],video['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('1080x1920 30fps required')
    if not audio or audio.get('sample_rate')!='48000' or not subtitle:
        raise ValueError('audio/subtitle track required')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise ValueError('video unreadable')
    output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-map','1:s:0',
         '-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-c:s','copy','-metadata:s:a:0','language=jpn',
         '-metadata:s:s:0','language=jpn','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0;changed=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            out=focus_frame(frame,count/30)
            if out is not frame:changed+=1
            proc.stdin.write(out.tobytes())
            count+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf8','replace');rc=proc.wait()
        if rc: raise RuntimeError('ffmpeg failed: '+err[-2000:])
    except Exception:
        proc.kill();raise
    finally: cap.release()
    if count!=691 or changed<40:raise RuntimeError(f'frame count or changed count wrong: {count}, {changed}')
    report.write_text(json.dumps({'genre':genre,'review_only':True,'source_sha256':sha256(source),
        'output_sha256':sha256(output),'frames':count,'camera_frames':changed,
        'roi':ROI,'keyframes':KEYFRAMES,'publication_approved':False},ensure_ascii=False,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--report',required=True);ap.add_argument('--genre',required=True)
    ap.add_argument('--review-only',action='store_true')
    a=ap.parse_args();render(a.source,a.output,a.report,a.genre,a.review_only)
