"""Review-only single-frame burned-caption dropout repair for ten TikTok genres.

Restores one caption frame from the immediately preceding readable frame only
when both neighbours are legible and the non-caption scene is stable.
Does NOT verify Japanese narration meaning, rights, or publication readiness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food',
          'product_comparison_lifestyle')
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'contains_personal_data': False}
DEFAULT_ROI = (250, 1560, 850, 1800)  # x1,y1,x2,y2 at 1080x1920

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def validate_manifest(manifest,genre,source,output):
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('Unsupported genre')
    if any(manifest.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Review-only safety policy missing or unsafe')
    if manifest.get('source_sha256') != sha256(source):
        raise ValueError('Source SHA256 mismatch')
    if Path(source).resolve()==Path(output).resolve():
        raise ValueError('Refuse to overwrite input')
    if Path(output).exists():raise FileExistsError('Output already exists')

def bright_count(frame,roi=DEFAULT_ROI,threshold=100):
    x1,y1,x2,y2=roi
    if not(0<=x1<x2<=frame.shape[1] and 0<=y1<y2<=frame.shape[0]):
        raise ValueError('Caption ROI outside frame')
    return int(np.count_nonzero(np.max(frame[y1:y2,x1:x2],axis=2)>threshold))

def stable_scene(prev,nxt):
    h,w=prev.shape[:2]
    a=prev[int(h*.13):int(h*.69):16,int(w*.05):int(w*.95):16]
    b=nxt[int(h*.13):int(h*.69):16,int(w*.05):int(w*.95):16]
    return float(np.mean(cv2.absdiff(a,b)))<18

def should_repair(prev,cur,nxt,roi=DEFAULT_ROI,min_visible=None,drop_fraction=.15):
    if min_visible is None:
        min_visible=max(40,int((roi[2]-roi[0])*(roi[3]-roi[1])*.027))
    p,c,n=[bright_count(f,roi) for f in (prev,cur,nxt)]
    return (p>=min_visible and n>=min_visible and
            c<min(p,n)*drop_fraction and stable_scene(prev,nxt))

def repair_frame(prev,cur,nxt,roi=DEFAULT_ROI):
    if not should_repair(prev,cur,nxt,roi):return cur,False
    x1,y1,x2,y2=roi
    out=cur.copy()
    out[y1:y2,x1:x2]=prev[y1:y2,x1:x2]
    return out,True

def probe(source):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=codec_name,width,height,r_frame_rate,sample_rate,nb_frames',
        '-show_entries','format=duration','-of','json',str(source)],text=True))
    v=next(s for s in d['streams'] if s['codec_name'] in ('h264','hevc','mpeg4'))
    a=next((s for s in d['streams'] if s['codec_name']=='aac'),None)
    if a is None:raise ValueError('Expected AAC narration stream')
    return v,a,d

def render(source,output,manifest,genre='ai_work',roi=DEFAULT_ROI):
    source,output=Path(source),Path(output)
    validate_manifest(manifest,genre,source,output)
    v,a,meta=probe(source)
    w,h=int(v['width']),int(v['height'])
    fps_num,fps_den=map(int,v['r_frame_rate'].split('/'))
    if fps_num/fps_den!=30 or (w,h)!=(1080,1920):
        raise ValueError('This reviewed preset requires 1080x1920 30fps')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise ValueError('Cannot decode input')
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{w}x{h}','-r','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    repaired=[];index=0
    try:
        ok,prev=cap.read();ok2,cur=cap.read()
        if not ok or not ok2:raise ValueError('Too few frames')
        proc.stdin.write(prev.tobytes());index=1
        while True:
            ok,nxt=cap.read()
            if not ok:break
            fixed,changed=repair_frame(prev,cur,nxt,roi)
            if changed:repaired.append(index)
            proc.stdin.write(fixed.tobytes())
            prev,cur=cur,nxt;index+=1
        proc.stdin.write(cur.tobytes());index+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait()!=0:raise RuntimeError(err[-3000:])
    except Exception:
        proc.kill();proc.wait()
        if output.exists():output.unlink()
        raise
    finally:cap.release()
    outv,outa,_=probe(output)
    if int(outv.get('nb_frames',0))!=index or outa['sample_rate']!=a['sample_rate']:
        raise AssertionError('A/V metadata mismatch')
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'frames':index,'repaired_frames':repaired,
            'repaired_count':len(repaired),'width':w,'height':h,
            'fps':30,'audio_codec':'aac','full_av_decode':True,
            'review_only':True,'publication_approved':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre),indent=2))
if __name__=='__main__':main()
