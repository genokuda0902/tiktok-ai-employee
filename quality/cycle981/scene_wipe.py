"""Cycle981: caption-safe left-to-right wipes at *verified hard cuts* only.
Review-only: never uploads source media, merges, approves, or posts.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES = ('ai_work','money','health','science','history','language',
          'career','psychology','travel','lifestyle')
REVIEWED_LAYOUTS = {'ai_work'}

def validate_config(width, height, fps, total, cuts, genre, synthetic=False):
    if genre not in GENRES: raise ValueError('Unknown genre')
    if genre not in REVIEWED_LAYOUTS and not synthetic:
        raise ValueError('Fail closed: layout not reviewed')
    if width<=0 or height<=0 or fps<=0 or total<10:
        raise ValueError('Invalid video')
    if cuts != sorted(set(cuts)) or any(c<6 or c>total-6 for c in cuts):
        raise ValueError('Invalid scene cuts')
    if any(b-a<12 for a,b in zip(cuts,cuts[1:])):
        raise ValueError('Cuts too close')

def feather_mask(width, progress, feather=48):
    if not 0<=progress<=1: raise ValueError('progress out of bounds')
    x=np.arange(width,dtype=np.float32)
    edge=progress*(width+feather)-feather/2
    z=np.clip((edge-x)/max(1,feather)+.5,0,1)
    return z*z*(3-2*z)

def compose_wipe(old,new,progress,top,bottom,feather=48):
    if old.shape!=new.shape or old.ndim!=3 or old.shape[2]!=3:
        raise ValueError('Mismatched frames')
    if not 0<=top<bottom<=old.shape[0]: raise ValueError('Bad ROI')
    alpha=feather_mask(old.shape[1],progress,feather)[None,:,None]
    out=(new if progress>=.5 else old).copy()
    out[top:bottom]=np.clip(old[top:bottom].astype(np.float32)*(1-alpha)+
        new[top:bottom].astype(np.float32)*alpha,0,255).astype(np.uint8)
    return out

def read_frame(cap,idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
    ok,f=cap.read()
    if not ok: raise RuntimeError('Cannot read frame '+str(idx))
    return f

def render(source,output,cuts,genre='ai_work',synthetic=False,
           top=100,bottom=1180,radius=3):
    if Path(source).resolve()==Path(output).resolve():
        raise ValueError('Source and output must differ')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('Cannot open source')
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    validate_config(w,h,fps,total,cuts,genre,synthetic)
    if not 0<=top<bottom<=h-80 or not 2<=radius<=10:
        raise ValueError('Caption protection / radius invalid')
    anchors={b:(read_frame(cap,b-1),read_frame(cap,b)) for b in cuts}
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','18','-pix_fmt','yuv420p','-frames:v',str(total),
         '-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=[]
    try:
        for i in range(total):
            ok,current=cap.read()
            if not ok: raise RuntimeError('Source ended at frame '+str(i))
            frame=current
            for b in cuts:
                if b-radius<=i<=b+radius:
                    old,new=anchors[b]
                    progress=(i-(b-radius)+1)/(2*radius+2)
                    frame=compose_wipe(current if i<b else old,
                        new if i<b else current,progress,top,bottom)
                    changed.append(i)
                    break
            p.stdin.write(frame.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode('utf-8','replace')
        if p.wait()!=0: raise RuntimeError('ffmpeg: '+err[-1000:])
    except Exception:
        if p.poll() is None: p.kill()
        raise
    finally:
        cap.release()
    return {'frames':total,'fps':fps,'size':[w,h],'cuts':cuts,
            'changed_frames':changed,'caption_protected_from_y':bottom,
            'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('source');a.add_argument('output')
    a.add_argument('--cuts',required=True)
    a.add_argument('--genre',default='ai_work',choices=GENRES)
    a.add_argument('--synthetic',action='store_true')
    a.add_argument('--top',type=int,default=100)
    a.add_argument('--bottom',type=int,default=1180)
    a.add_argument('--radius',type=int,default=3)
    args=a.parse_args()
    print(json.dumps(render(args.source,args.output,
        [int(x) for x in args.cuts.split(',')],args.genre,args.synthetic,
        args.top,args.bottom,args.radius),ensure_ascii=False))
