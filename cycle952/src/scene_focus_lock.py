"""Review-only step/caption alignment repair; reimplementation, NOT v33 source."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES=('ai_work','finance','history','science','health','travel','food','career','education','lifestyle')
FPS=30
FIX=(3.78,5.76)
CAPTION_TOP=1250
PANEL=(0,0,1080,1240)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def validate(manifest):
    required={'genre','source_sha256','source_scene','caption','active_step','geometry_reviewed'}
    if not required.issubset(manifest): raise ValueError('missing provenance')
    if manifest['genre'] not in GENRES: raise ValueError('unsupported genre')
    if manifest['geometry_reviewed'] is not True: raise ValueError('unreviewed geometry')
    if manifest['source_scene']!=2 or manifest['active_step']!=1: raise ValueError('wrong step')
    if manifest['caption']!='まず、繰り返している作業を書き出そう。': raise ValueError('caption mismatch')
    if len(manifest['source_sha256'])!=64: raise ValueError('missing source sha')
    return True

def focus_frame(frame,reference,t):
    if not FIX[0]<=t<=FIX[1]: return frame
    h,w=frame.shape[:2]
    if (w,h)!=(1080,1920): raise ValueError('unsupported geometry')
    x1,y1,x2,y2=PANEL
    progress=np.clip((t-FIX[0])/(FIX[1]-FIX[0]),0,1)
    scale=1.0+0.020*progress
    cx,cy=540,620
    matrix=np.float32([[scale,0,cx*(1-scale)],[0,scale,cy*(1-scale)]])
    corrected=cv2.warpAffine(reference,matrix,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    mask=np.zeros((h,w),np.uint8)
    cv2.rectangle(mask,(x1,y1),(x2,y2),255,-1)
    mask=cv2.GaussianBlur(mask,(0,0),4).astype(np.float32)/255
    fade=min(1.0,max(0.0,(t-FIX[0])/0.20))
    mask*=fade
    mask[CAPTION_TOP:,:]=0
    area=np.s_[max(0,y1-35):min(h,y2+35),max(0,x1-35):min(w,x2+35)]
    a=mask[area][...,None]
    result=frame.copy()
    result[area]=np.clip(frame[area].astype(np.float32)*(1-a)+corrected[area].astype(np.float32)*a,0,255).astype(np.uint8)
    return result

def render(source,output,manifest):
    validate(manifest)
    if sha256(source)!=manifest['source_sha256']: raise ValueError('source SHA mismatch')
    cap=cv2.VideoCapture(str(source))
    fps=cap.get(cv2.CAP_PROP_FPS)
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if abs(fps-FPS)>.01 or count!=691: raise ValueError('unexpected timing')
    cap.set(cv2.CAP_PROP_POS_FRAMES,99)
    ok,reference=cap.read()
    if not ok: raise RuntimeError('missing reference')
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    temp=Path(output).with_suffix('.video.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(temp)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(count):
            ok,frame=cap.read()
            if not ok: raise RuntimeError('truncated source')
            p.stdin.write(focus_frame(frame,reference,i/FPS).tobytes())
    finally:
        p.stdin.close()
        cap.release()
    if p.wait()!=0: raise RuntimeError('encoder failed')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(temp),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',str(output)],check=True)
    temp.unlink()
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),'modified_range_seconds':list(FIX),'frames':count,'independent_japanese_asr':'UNVERIFIED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for key in ('source','output','manifest','qa'): parser.add_argument('--'+key,required=True)
    args=parser.parse_args()
    report=render(Path(args.source),Path(args.output),json.loads(Path(args.manifest).read_text(encoding='utf-8')))
    Path(args.qa).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
