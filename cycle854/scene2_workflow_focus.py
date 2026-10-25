"""cycle854: offline 10-genre cinematic task-focus scene for HUMAN REVIEW ONLY.

Never downloads, publishes or uploads media. A source video and strict local
SHA256 policy manifest are required; public release remains unapproved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison_lifestyle')
PALETTES = {g:(32+(i*7)%45,200-(i*5)%40,218-(i*6)%40) for i,g in enumerate(GENRES)}
POLICY = {'review_only':True,'publication_approved':False,
          'automatic_posting':False,'external_upload':False,
          'source_rights_reviewed':False,'contains_personal_data':False,
          'fictional_workflow_example':True}
PANEL = (86,476,994,1234)   # no modifications to upper heading or lower Japanese captions
WINDOW = (89,170)            # 2.967s to 5.667s (81 frames)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
LABELS = ('集計・入力', '資料の作成', '定型メール')


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))


def streams(path):
    s=probe(path)['streams']
    return (next((x for x in s if x['codec_type']=='video'),None),
            next((x for x in s if x['codec_type']=='audio'),None))


def beat(frame, total):
    if not isinstance(frame,int) or not isinstance(total,int) or total<3 or not 0<=frame<total:
        raise ValueError('invalid frame/total')
    return min(2,3*frame//total)


def validate(source, output, manifest, genre, window, background_frame):
    source=Path(source);output=Path(output)
    if genre not in GENRES or len(set(GENRES))!=10:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError('missing local source video')
    if manifest != {**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('strict source SHA / rights manifest mismatch')
    if output.exists() or source.resolve()==output.resolve():
        raise ValueError('overwriting a video is forbidden')
    v,a=streams(source)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name']) != ('h264',1080,1920,'30/1','aac'):
        raise ValueError('input must be H264 1080x1920 30fps + AAC')
    n=int(v['nb_frames'])
    if len(window)!=2 or not all(type(x)==int for x in window) or not 0<=window[0]<window[1]<=n:
        raise ValueError('invalid window')
    if type(background_frame)!=int or not window[0]<=background_frame<window[1]:
        raise ValueError('background must be from source scene window')
    return n


def load_background(source, index):
    cap=cv2.VideoCapture(str(source))
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES,index)
        ok,fr=cap.read()
        if not ok:raise RuntimeError('cannot read source scene background')
        x0,y0,x1,y1=PANEL
        return Image.fromarray(cv2.cvtColor(fr[y0:y1,x0:x1],cv2.COLOR_BGR2RGB))
    finally:cap.release()


def ease(t):
    t=max(0.,min(1.,float(t)))
    return t*t*(3-2*t)


def make_panel(photo, local, total, genre):
    """Original cinematic glass-card motion, source background only; no new external assets."""
    if genre not in GENRES:raise ValueError('unknown genre')
    b=beat(local,total)
    w,h=908,758
    if photo.size!=(w,h):raise ValueError('background must be exact source panel size')
    # Gentle Ken Burns pan, deliberately constrained to avoid upscaling beyond 1.045.
    scale=1.025+0.020*(local/max(1,total-1))
    nw,nh=round(w*scale),round(h*scale)
    enlarged=photo.resize((nw,nh),Image.Resampling.BICUBIC)
    dx=round((nw-w)*(0.35+0.25*local/max(1,total-1)))
    dy=round((nh-h)*0.45)
    bg=enlarged.crop((dx,dy,dx+w,dy+h)).filter(ImageFilter.GaussianBlur(3.0))
    # Warm photograph on left, contrast-corrected glass panel on right.
    a=np.asarray(bg,dtype=np.float32).copy()
    yy=np.linspace(0,1,h,dtype=np.float32)[:,None]
    xx=np.linspace(0,1,w,dtype=np.float32)[None,:]
    shade=(0.45+0.16*xx+0.07*yy)[...,None]
    a=np.clip(a*(1-shade),0,255).astype('uint8')
    out=Image.fromarray(a,'RGB')
    d=ImageDraw.Draw(out)
    font=lambda sz:ImageFont.truetype(FONT,sz)
    accent=PALETTES[genre]
    # Soft cinematic depth using a small glow, drawn only inside safe panel.
    glow=Image.new('RGBA',(w,h),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((-210,300,450,960),fill=(*accent,40))
    glow=glow.filter(ImageFilter.GaussianBlur(75))
    out=Image.alpha_composite(out.convert('RGBA'),glow)
    d=ImageDraw.Draw(out)
    d.rounded_rectangle((36,34,872,724),radius=35,fill=(4,16,28,218),outline=(*accent,235),width=3)
    d.rounded_rectangle((67,67,492,119),radius=16,fill=(*accent,205))
    d.text((279,93),'STEP 01  /  見つける',font=font(28),anchor='mm',fill=(255,255,255,255))
    d.text((72,150),'毎日くり返す作業',font=font(49),fill=(249,251,255,255),stroke_width=1,stroke_fill=(6,25,37,255))
    d.text((74,222),'まず、ひとつ書き出す。',font=font(31),fill=(194,222,232,255))
    row_top=295
    for i,label in enumerate(LABELS):
        y=row_top+i*110
        active=i==b
        fill=(16,67,80,250) if active else (12,35,52,224)
        outline=(*accent,255) if active else (67,92,109,180)
        d.rounded_rectangle((66,y,840,y+91),radius=19,fill=fill,outline=outline,width=4 if active else 2)
        d.rounded_rectangle((87,y+21,133,y+67),radius=11,fill=(*accent,255) if active else (45,65,83,255))
        if active:
            d.line((99,y+44,109,y+54,123,y+34),fill=(255,255,255,255),width=6,joint='curve')
        else:d.text((110,y+44),str(i+1),font=font(26),anchor='mm',fill=(207,221,231,255))
        d.text((159,y+46),label,font=font(38),anchor='lm',fill=(255,255,255,255) if active else (195,209,219,255))
        if active:
            # Deliberate small animation; highlighted row is a 0.9s editorial beat.
            t=(local-(i*total//3))/max(1,total//3)
            pulse=round(14*ease(t))
            d.rounded_rectangle((652,y+23,813,y+67),radius=12,fill=(17,111,112,255))
            d.text((733,y+45),'ここに注目',font=font(23),anchor='mm',fill=(255,255,255,255))
            d.line((159,y+77,159+min(350,pulse*25),y+77),fill=(*accent,255),width=5)
    d.rounded_rectangle((68,649,840,699),radius=14,fill=(9,55,68,248))
    d.text((454,674),'全部ではなく、まず1つ。',font=font(30),anchor='mm',fill=(237,252,251,255))
    return cv2.cvtColor(np.asarray(out.convert('RGB')),cv2.COLOR_RGB2BGR)


def composite(frame, panel):
    if frame.shape!=(1920,1080,3):raise ValueError('bad source frame dimensions')
    if panel.shape!=(758,908,3):raise ValueError('bad panel dimensions')
    x0,y0,x1,y1=PANEL
    out=frame.copy();out[y0:y1,x0:x1]=panel
    return out


def render(source,output,manifest,genre='ai_work',window=WINDOW,background_frame=108):
    source=Path(source);output=Path(output)
    n=validate(source,output,manifest,genre,window,background_frame)
    bg=load_background(source,background_frame)
    cap=cv2.VideoCapture(str(source))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
        '-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264',
        '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for i in range(n):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('input truncated')
            if window[0]<=i<window[1]:
                panel=make_panel(bg,i-window[0],window[1]-window[0],genre)
                frame=composite(frame,panel);changed+=1
            p.stdin.write(frame.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError('ffmpeg encode failed: '+err[-1500:])
    except Exception:
        p.kill();p.wait();output.unlink(missing_ok=True);raise
    finally:cap.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=streams(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':raise RuntimeError('stream verification failed')
    return {'cycle':854,'genre':genre,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'frames':n,'changed_frames':changed,'window':list(window),'beats':3,
            'full_av_decode':True,'source_rights_reviewed':False,
            'independent_japanese_asr_verified':False,'semantic_subtitle_sync_verified':False,
            'smartphone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):p.add_argument('--'+k,required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--window',type=int,nargs=2,default=list(WINDOW))
    p.add_argument('--background-frame',type=int,default=108)
    a=p.parse_args()
    result=render(a.source,a.output,json.loads(Path(a.manifest).read_text(encoding='utf-8')),
                  a.genre,tuple(a.window),a.background_frame)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))