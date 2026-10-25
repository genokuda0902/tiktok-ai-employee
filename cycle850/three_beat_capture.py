"""Review-only 3-beat close-up edit of a *fictional, locally captured* UI clip.

Generic 10-genre template. It NEVER changes source voice or captions and
refuses unknown assets, overwrites, automatic publishing, and missing consent.
The source clip and any private assets must remain outside public GitHub.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_work','sales_business','beauty','romance','saving','career',
        'wellness','science','travel_food','product_comparison_lifestyle')
POLICY={'review_only':True,'publication_approved':False,'automatic_posting':False,
        'external_upload':False,'source_rights_reviewed':False,
        'contains_personal_data':False,'capture_is_fictional':True}
WINDOW=(336,422)
PANEL=(86,476,994,1234)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SHOTS=(('01 / 03  全体を見る',1.0,(350,380)),
       ('02 / 03  数字を追う',1.35,(305,365)),
       ('03 / 03  合計を確認',1.65,(310,470)))

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def frame_count(path):
    return int(next(x for x in probe(path)['streams'] if x['codec_type']=='video')['nb_frames'])

def validate(source,capture,output,manifest,genre,window):
    source,capture,output=map(Path,(source,capture,output))
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('invalid genre')
    if manifest!={**POLICY,'source_sha256':sha256(source),'capture_sha256':sha256(capture)}:
        raise ValueError('unapproved or changed asset manifest')
    if output.exists() or output.resolve() in (source.resolve(),capture.resolve()):
        raise ValueError('refuse output overwrite')
    if len(window)!=2 or not all(type(x) is int for x in window) or not 0<=window[0]<window[1]:
        raise ValueError('invalid frame window')
    s=probe(source);v=next((x for x in s['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in s['streams'] if x['codec_type']=='audio'),None)
    if not v or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1') or not a or a['codec_name']!='aac':
        raise ValueError('source requires 1080x1920 30fps H264 and AAC')
    n=int(v['nb_frames'])
    c=probe(capture);cv=next((x for x in c['streams'] if x['codec_type']=='video'),None)
    if not cv or cv['width']<700 or cv['height']<700 or cv['r_frame_rate']!='30/1':
        raise ValueError('capture must be local 30fps UI')
    if window[1]>n or window[1]-window[0]>int(cv['nb_frames']):
        raise ValueError('window outside source or capture')
    return n

def shot_index(local_index,total):
    if not 0<=local_index<total:raise ValueError('out of bounds')
    return min(2,(local_index*3)//total)

def crop_focus(capture,zoom,center,shape):
    h,w=capture.shape[:2];target_w,target_h=shape
    base_w,base_h=700,round(700*target_h/target_w)
    cw,ch=round(base_w/zoom),round(base_h/zoom)
    if cw>w or ch>h:raise ValueError('capture too small')
    x=max(0,min(w-cw,round(center[0]-cw/2)))
    y=max(0,min(h-ch,round(center[1]-ch/2)))
    return cv2.resize(capture[y:y+ch,x:x+cw],(target_w,target_h),interpolation=cv2.INTER_AREA)

def make_badge(text,step,width):
    badge=Image.new('RGBA',(width,86),(0,0,0,0));d=ImageDraw.Draw(badge)
    d.rounded_rectangle((10,8,width-10,76),radius=15,fill=(3,28,43,245),outline=(64,217,210,255),width=3)
    font=ImageFont.truetype(FONT,32)
    d.text((width//2,42),text,font=font,anchor='mm',fill=(250,255,255,255))
    d.rectangle((12,70,12+(width-24)*step/3,75),fill=(42,220,192,255))
    return np.array(badge)[:,:, [2,1,0,3]].copy()

def composite(frame,capture,local_index,total,badges):
    if frame.shape[:2]!=(1920,1080):raise ValueError('source shape')
    out=frame.copy();step=shot_index(local_index,total)
    x0,y0,x1,y1=PANEL
    text,zoom,center=SHOTS[step]
    ui=crop_focus(capture,zoom,center,(x1-x0,y1-y0))
    out[y0:y1,x0:x1]=ui
    # Opaque label within the footage panel; header and Japanese captions untouched.
    badge=badges[step];bh,bw=badge.shape[:2]
    roi=out[y0+10:y0+10+bh,x0+10:x0+10+bw]
    alpha=badge[:,:,3:4].astype(np.float32)/255
    roi[:]=(roi.astype(np.float32)*(1-alpha)+badge[:,:,:3]*alpha).astype(np.uint8)
    cv2.rectangle(out,(x0+3,y0+3),(x1-3,y1-3),(37,201,199),3)
    return out

def render(source,capture,output,manifest,genre='ai_work',window=WINDOW):
    source,capture,output=map(Path,(source,capture,output))
    n=validate(source,capture,output,manifest,genre,window)
    cap=cv2.VideoCapture(str(source));demo=cv2.VideoCapture(str(capture))
    x0,y0,x1,y1=PANEL
    badges=[make_badge(s[0],i+1,x1-x0-20) for i,s in enumerate(SHOTS)]
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0
    try:
        for idx in range(n):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('early source EOF')
            if window[0]<=idx<window[1]:
                ok,cf=demo.read()
                if not ok:raise RuntimeError('early capture EOF')
                frame=composite(frame,cf,idx-window[0],window[1]-window[0],badges)
                count+=1
            p.stdin.write(frame.tobytes())
        p.stdin.close();err=p.stderr.read().decode(errors='replace')
        if p.wait():raise RuntimeError('ffmpeg: '+err[-1000:])
    except Exception:
        p.kill();p.wait();output.unlink(missing_ok=True);raise
    finally:cap.release();demo.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    if frame_count(output)!=n:raise RuntimeError('frame count mismatch')
    return {'cycle':850,'source_sha256':sha256(source),'capture_sha256':sha256(capture),
            'output_sha256':sha256(output),'frames':n,'changed_frames':count,
            'three_shots':list(SHOTS[i][0] for i in range(3)),
            'cut_frames':[window[0]+(window[1]-window[0]+2)//3,window[0]+((window[1]-window[0])*2+2)//3],
            'genre':genre,'resolution':'1080x1920','video':'H264 30fps',
            'audio':'AAC stream copied','full_av_decode':True,'publication_approved':False,
            'independent_japanese_asr_verified':False,'rights_cleared':False,
            'smartphone_playback_verified':False,'quality_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for x in ('source','capture','output','report'):ap.add_argument('--'+x,required=True)
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--window',default='336,422')
    a=ap.parse_args();s,c=Path(a.source),Path(a.capture)
    w=tuple(map(int,a.window.split(',')))
    result=render(s,c,a.output,{**POLICY,'source_sha256':sha256(s),'capture_sha256':sha256(c)},a.genre,w)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))