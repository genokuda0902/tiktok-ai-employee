"""Offline, review-only replacement of a static spreadsheet still with genuine local Calc capture.

The input capture must be generated from fictional data and remain local.  This
module only composites video into the middle visual panel; it never touches the
Japanese burnt captions, original audio, or posting/approval state.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_work','sales_business','beauty','romance','saving','career',
        'wellness','science','travel_food','product_comparison_lifestyle')
POLICY={'review_only':True,'publication_approved':False,'automatic_posting':False,
        'external_upload':False,'source_rights_reviewed':False,
        'contains_personal_data':False,'capture_is_fictional':True}
DEFAULT_WINDOW=(336,422)
# Compositing is strictly within image area; header <=300 and captions >=1540 untouched.
CARD=(85,475,995,1235)
LABEL=(90,1290,990,1380)
CAPTION_START=1540
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
       '-show_format','-of','json',str(path)],text=True))

def validate(source,capture,output,manifest,genre,window):
    source,capture,output=map(Path,(source,capture,output))
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('unsupported genre')
    if manifest!={**POLICY,'source_sha256':sha256(source),'capture_sha256':sha256(capture)}:
        raise ValueError('fail-closed manifest mismatch')
    if len(window)!=2 or not all(isinstance(x,int) for x in window) or not 0<=window[0]<window[1]:
        raise ValueError('invalid window')
    if output.exists() or output.resolve() in (source.resolve(),capture.resolve()):
        raise ValueError('refuse overwrite')
    s=probe(source);v=next((a for a in s['streams'] if a['codec_type']=='video'),None)
    a=next((a for a in s['streams'] if a['codec_type']=='audio'),None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1') or a['codec_name']!='aac':
        raise ValueError('requires 1080x1920 30fps H264 + AAC')
    total=int(v.get('nb_frames') or round(float(s['format']['duration'])*30))
    if window[1]>total:raise ValueError('window exceeds source')
    c=probe(capture);cv=next((a for a in c['streams'] if a['codec_type']=='video'),None)
    if not cv or cv['width']<660 or cv['height']<700 or cv['r_frame_rate']!='30/1':
        raise ValueError('invalid 30fps local Calc capture')
    capframes=int(cv.get('nb_frames') or round(float(c['format']['duration'])*30))
    if capframes<window[1]-window[0]:raise ValueError('capture too short')
    return total

def make_label():
    w,h=900,90
    canvas=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((0,6,w-1,h-5),radius=22,fill=(2,34,49,247),outline=(35,211,203,255),width=3)
    font=ImageFont.truetype(FONT,31)
    d.text((w//2,44),'実際のCalc操作  ／  架空データ',font=font,anchor='mm',fill=(235,255,255,255))
    return np.array(canvas)[:,:, [2,1,0,3]].copy()

def composite(frame,capture_frame,label):
    """Never change top header or bottom caption; overlay a clean real UI capture."""
    if frame.shape[:2]!=(1920,1080):raise ValueError('wrong source shape')
    out=frame.copy();x0,y0,x1,y1=CARD
    cv2.rectangle(out,(80,415),(1000,1440),(41,28,4),thickness=-1)
    cv2.rectangle(out,(80,415),(1000,1440),(96,81,26),thickness=3)
    crop=capture_frame[85:695,0:660]
    if crop.shape[:2]!=(610,660):raise ValueError('invalid capture crop')
    ui=cv2.resize(crop,(x1-x0-14,y1-y0-14),interpolation=cv2.INTER_AREA)
    cv2.rectangle(out,(x0-4,y0-4),(x1+4,y1+4),(3,29,44),thickness=-1)
    cv2.rectangle(out,(x0-4,y0-4),(x1+4,y1+4),(46,203,199),thickness=4)
    out[y0+7:y1-7,x0+7:x1-7]=ui
    lx0,ly0,lx1,ly1=LABEL
    roi=out[ly0:ly1,lx0:lx1]
    alpha=label[:,:,3:4].astype(np.float32)/255
    roi[:]=np.clip(roi.astype(np.float32)*(1-alpha)+label[:,:,:3].astype(np.float32)*alpha,0,255).astype(np.uint8)
    return out

def render(source,capture,output,manifest,genre='ai_work',window=DEFAULT_WINDOW):
    source,capture,output=map(Path,(source,capture,output))
    total=validate(source,capture,output,manifest,genre,window)
    cap=cv2.VideoCapture(str(source));demo=cv2.VideoCapture(str(capture))
    label=make_label()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for idx in range(total):
            ok,frame=cap.read()
            if not ok:raise RuntimeError(f'early source EOF frame={idx}')
            if window[0]<=idx<window[1]:
                ok,demo_frame=demo.read()
                if not ok:raise RuntimeError(f'early capture EOF frame={idx}')
                frame=composite(frame,demo_frame,label);changed+=1
            p.stdin.write(frame.tobytes())
        p.stdin.close();err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError('ffmpeg: '+err[-1800:])
    except Exception:
        p.kill();p.wait();output.unlink(missing_ok=True);raise
    finally:
        cap.release();demo.release()
    out=probe(output)
    v=next(s for s in out['streams'] if s['codec_type']=='video')
    a=next(s for s in out['streams'] if s['codec_type']=='audio')
    if int(v['nb_frames'])!=total or a['codec_name']!='aac':
        output.unlink(missing_ok=True);raise RuntimeError('output stream mismatch')
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    return {'source_sha256':sha256(source),'capture_sha256':sha256(capture),
        'output_sha256':sha256(output),'frames':total,'changed_frames':changed,
        'window':list(window),'genre':genre,'resolution':'1080x1920',
        'video':'H264/30fps','audio':'AAC stream copied','full_av_decode':True,
        'capture_provenance':'declared fictional local capture; not independently authenticated',
        'publication_approved':False,'automatic_posting':False,'external_upload':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True)
    ap.add_argument('--capture',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--report',required=True);ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--window',default='336,422')
    a=ap.parse_args();win=tuple(map(int,a.window.split(',')))
    src=Path(a.source);capture=Path(a.capture)
    result=render(src,capture,a.output,{**POLICY,'source_sha256':sha256(src),'capture_sha256':sha256(capture)},a.genre,win)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
