#!/usr/bin/env python3
"""Ghost-free luminance guard for manifest-declared hard cuts; review only.

Unlike a cross-dissolve, each output frame uses exactly one source frame.
Only a feathered artwork ROI changes; no face/UI geometry is composited.
The source must have approved provenance for any public use; this tool does
NOT grant rights or publishing permission.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import cv2
import numpy as np

GENRES = ('ai_work', 'business', 'money', 'learning', 'health', 'life',
          'travel', 'food', 'tech', 'history')
ROI = (24, 255, 1032, 855)
WINDOW = 6
THRESHOLD = 55.0

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def luma(frame, roi=ROI):
    x,y,w,h=roi
    return float(cv2.cvtColor(frame[y:y+h:4,x:x+w:4],cv2.COLOR_BGR2GRAY).mean())

def matte_for(roi=ROI, feather=36):
    _,_,w,h=roi
    if feather<1 or 2*feather>=min(w,h):raise ValueError('invalid feather')
    xs=np.minimum(np.arange(w),np.arange(w)[::-1])/feather
    ys=np.minimum(np.arange(h),np.arange(h)[::-1])/feather
    return np.minimum(1,np.minimum(xs[None,:],ys[:,None])).astype('float32')[:,:,None]

def apply_single_source(frame, shift, roi=ROI, matte=None):
    if not np.isfinite(shift) or abs(shift)>90:raise ValueError('unsafe luma shift')
    if abs(shift)<0.01:return frame
    x,y,w,h=roi
    if matte is None:matte=matte_for(roi)
    out=frame.copy()
    crop=frame[y:y+h,x:x+w].astype('float32')
    out[y:y+h,x:x+w]=np.clip(np.rint(crop+shift*matte),0,255).astype('uint8')
    return out

def make_shifts(source,cuts,threshold=THRESHOLD,window=WINDOW):
    if not cuts or sorted(set(cuts))!=cuts:raise ValueError('cuts must be sorted and unique')
    if threshold<30 or threshold>150 or window<2 or window>12:raise ValueError('unsafe parameters')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise ValueError('cannot decode source')
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if any(c<window or c+window>=n for c in cuts):raise ValueError('cut out of range')
    shifts={}; stats=[]
    try:
        for c in cuts:
            cap.set(cv2.CAP_PROP_POS_FRAMES,c-1)
            ok,a=cap.read(); ok2,b=cap.read()
            if not(ok and ok2):raise ValueError('cut decode failed')
            left,right=luma(a),luma(b); jump=abs(right-left)
            active=jump>=threshold
            stats.append({'cut':c,'source_before':round(left,3),'source_after':round(right,3),
                          'source_jump':round(jump,3),'guarded':active})
            if active:
                half=(right-left)/2
                if abs(half)>90:raise ValueError('excessive shift')
                for k in range(window):
                    shifts[c-window+k]=shifts.get(c-window+k,0)+half*(k+1)/window
                    shifts[c+k]=shifts.get(c+k,0)-half*(window-k)/window
    finally:cap.release()
    if not shifts:raise ValueError('no qualifying cut; fail closed')
    return shifts,stats

def render(source,output,report,genre,cuts,review_only=False,threshold=THRESHOLD,window=WINDOW):
    source,output,report=map(Path,(source,output,report))
    if not review_only or genre not in GENRES:raise ValueError('review-only ten-genre gate')
    if source.resolve()==output.resolve() or not source.is_file():raise ValueError('invalid source/output')
    m=probe(source);v=next((s for s in m['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in m['streams'] if s['codec_type']=='audio'),None)
    s=next((s for s in m['streams'] if s['codec_type']=='subtitle'),None)
    if not v or (v.get('width'),v.get('height'),v.get('r_frame_rate'))!=(1080,1920,'30/1'):
        raise ValueError('1080x1920 30fps required')
    if not a or a.get('sample_rate')!='48000' or not s:raise ValueError('48kHz audio and subtitle required')
    frames=int(v.get('nb_frames') or 0)
    shifts,stats=make_shifts(source,cuts,threshold,window)
    output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','bgr24',
         '-video_size','1080x1920','-framerate','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-map','1:s:0','-c:v','libx264','-preset','veryfast',
         '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-c:s','copy',
         '-metadata:s:a:0','language=jpn','-metadata:s:s:0','language=jpn',
         '-frames:v',str(frames),'-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    cap=cv2.VideoCapture(str(source));matte=matte_for();written=0
    try:
        for i in range(frames):
            ok,frame=cap.read()
            if not ok:raise ValueError('early video EOF')
            out=apply_single_source(frame,shifts.get(i,0),matte=matte)
            p.stdin.write(out.tobytes());written+=1
        p.stdin.close();err=p.stderr.read().decode('utf8','replace')
        if p.wait()!=0:raise RuntimeError('ffmpeg failed: '+err[-2000:])
    except Exception:
        if not p.stdin.closed:p.stdin.close()
        p.kill();p.wait();raise
    finally:cap.release()
    outmeta=probe(output)
    actual=int(next(s for s in outmeta['streams'] if s['codec_type']=='video')['nb_frames'])
    if actual!=frames or written!=frames:raise ValueError('frame count mismatch')
    result={'genre':genre,'review_only':True,'publication_approved':False,
            'source_sha256':digest(source),'output_sha256':digest(output),
            'frames':frames,'seconds':float(outmeta['format']['duration']),
            'method':'single-source exposure compensation (no cross-dissolve)',
            'window':window,'threshold':threshold,'cut_stats':stats,
            'independent_asr_verified':False,'phone_playback_verified':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--cuts',required=True);p.add_argument('--review-only',action='store_true',required=True)
    a=p.parse_args();print(json.dumps(render(a.input,a.output,a.report,a.genre,
        [int(x) for x in a.cuts.split(',')],a.review_only),ensure_ascii=False))
