"""Review-only, ten-genre reusable repair for ghosted text/UI transitions.

Replace a short dissolving UI region with adjacent *existing* clean frames.
Leave the burned-in Japanese caption region and original AAC stream untouched.
No media is uploaded or approved for posting by this module.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'contains_personal_data': False}
BASELINE_FRAMES = 691
BOUNDARIES = (89,170,249,336,422,511,588)
CAPTION_START_Y = 1540

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
        '-show_format','-of','json',str(path)],text=True))

def validate(source,output,manifest,genre,boundaries,halfwidth):
    source,output=Path(source),Path(output)
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('unsupported genre')
    if manifest != {**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('fail-closed source SHA or safety policy mismatch')
    if source.resolve()==output.resolve() or output.exists():
        raise ValueError('refuse overwrite')
    if not isinstance(halfwidth,int) or not 1<=halfwidth<=10:
        raise ValueError('invalid transition width')
    if not boundaries or tuple(sorted(set(boundaries)))!=tuple(boundaries):
        raise ValueError('invalid boundaries')
    m=probe(source)
    v=next((s for s in m['streams'] if s.get('codec_type')=='video'),None)
    a=next((s for s in m['streams'] if s.get('codec_type')=='audio'),None)
    if not v or not a or a['codec_name']!='aac' or v['width']!=1080 or v['height']!=1920:
        raise ValueError('requires 1080x1920 H264+AAC review source')
    if v['codec_name']!='h264' or v['r_frame_rate']!='30/1':
        raise ValueError('requires 30fps H264')
    return int(v.get('nb_frames') or round(float(m['format']['duration'])*30))

def anchors(source,boundaries,halfwidth):
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('cannot read source')
    frames={}
    for b in boundaries:
        for idx in (b-halfwidth-2,b+halfwidth+2):
            cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
            ok,frame=cap.read()
            if not ok:raise RuntimeError(f'anchor missing: {idx}')
            frames[idx]=frame
    cap.release()
    return frames

def repair_region(frame,index,boundaries,clean,halfwidth,caption_start=CAPTION_START_Y):
    for b in boundaries:
        if b-halfwidth<=index<=b+halfwidth:
            src=clean[b-halfwidth-2] if index<b else clean[b+halfwidth+2]
            out=frame.copy()
            out[:caption_start,:,:]=src[:caption_start,:,:]
            return out,b
    return frame,None

def render(source,output,manifest,genre='ai_work',boundaries=BOUNDARIES,halfwidth=10):
    source,output=Path(source),Path(output)
    total=validate(source,output,manifest,genre,boundaries,halfwidth)
    if boundaries[0]<=halfwidth+2 or boundaries[-1]>=total-halfwidth-2:
        raise ValueError('unsafe boundary')
    clean=anchors(source,boundaries,halfwidth)
    cap=cv2.VideoCapture(str(source))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30',
         '-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    modified=[]
    try:
        for idx in range(total):
            ok,frame=cap.read()
            if not ok:raise RuntimeError(f'early end at frame {idx}')
            frame,b=repair_region(frame,idx,boundaries,clean,halfwidth)
            if b is not None:modified.append(idx)
            p.stdin.write(frame.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError(err[-1500:])
    except Exception:
        p.kill();p.wait();output.unlink(missing_ok=True);raise
    finally:
        cap.release()
    result=probe(output)
    vv=next(s for s in result['streams'] if s['codec_type']=='video')
    aa=next(s for s in result['streams'] if s['codec_type']=='audio')
    if int(vv.get('nb_frames',-1))!=total or aa['codec_name']!='aac':
        output.unlink(missing_ok=True);raise RuntimeError('output A/V mismatch')
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True,stdout=subprocess.DEVNULL)
    return {'genre':genre,'frames':total,'fps':30,'resolution':'1080x1920',
            'modified_frames':modified,'boundaries':list(boundaries),
            'audio_codec':'aac','full_av_decode':True,'output_sha256':sha256(output),
            'publication_approved':False,'external_upload':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--boundaries',default=','.join(map(str,BOUNDARIES)))
    ap.add_argument('--report',required=True)
    a=ap.parse_args();b=tuple(map(int,a.boundaries.split(',')))
    source=Path(a.source)
    result=render(source,a.output,{**POLICY,'source_sha256':sha256(source)},a.genre,b)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='modified_frames'},ensure_ascii=False))
