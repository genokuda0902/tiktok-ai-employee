"""cycle855: review-only, three-beat evidence-led hook from *local* source frames.

No media downloads, publication, third-party APIs or automatic posting.
Source media must have a SHA-pinned, fail-closed review manifest.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = ('ai_work','sales_business','beauty','romance','saving','career','wellness','science','travel_food','product_comparison_lifestyle')
PALETTES = {g: (40+(i*9)%80, 195-(i*6)%60, 224-(i*7)%60) for i,g in enumerate(GENRES)}
POLICY = {'review_only':True,'publication_approved':False,'automatic_posting':False,
          'external_upload':False,'source_rights_reviewed':False,
          'contains_personal_data':False,'fictional_workflow_example':True}
PANEL=(86,476,994,1234)
WINDOW=(0,89)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def streams(path):
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
    s=p['streams']
    return next((x for x in s if x['codec_type']=='video'),None),next((x for x in s if x['codec_type']=='audio'),None)

def validate(source,output,manifest,genre,window,desk_frame,evidence_frame):
    source=Path(source);output=Path(output)
    if genre not in GENRES or len(GENRES)!=10: raise ValueError('unknown genre')
    if not source.is_file(): raise FileNotFoundError('source missing')
    if manifest!={**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('source SHA / strict review policy mismatch')
    if source.resolve()==output.resolve() or output.exists(): raise ValueError('no overwrite')
    v,a=streams(source)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',1080,1920,'30/1','aac'):
        raise ValueError('requires H264 1080x1920 30fps and AAC')
    n=int(v['nb_frames'])
    if len(window)!=2 or not all(type(x)==int for x in window) or not 0<=window[0]<window[1]<=n:
        raise ValueError('invalid window')
    if window[1]-window[0]<9:raise ValueError('three beats need >=9 frames')
    if any(type(i)!=int or not 0<=i<n for i in (desk_frame,evidence_frame)):
        raise ValueError('invalid source frame')
    return n

def frame_crop(path,index):
    c=cv2.VideoCapture(str(path))
    try:
        c.set(cv2.CAP_PROP_POS_FRAMES,index)
        ok,f=c.read()
        if not ok:raise RuntimeError('frame unavailable')
        x0,y0,x1,y1=PANEL
        return Image.fromarray(cv2.cvtColor(f[y0:y1,x0:x1],cv2.COLOR_BGR2RGB))
    finally:c.release()

def font(sz):return ImageFont.truetype(FONT,sz)

def fit_cover(im,w,h,zoom=1.0):
    scale=max(w/im.width,h/im.height)*zoom
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BICUBIC)
    x=(im.width-w)//2;y=(im.height-h)//2
    return im.crop((x,y,x+w,y+h))

def bg_frame(desk,accent):
    im=fit_cover(desk,908,758).filter(ImageFilter.GaussianBlur(2.0)).convert('RGBA')
    overlay=Image.new('RGBA',im.size,(4,13,27,165))
    return Image.alpha_composite(im,overlay)

def panel_beat(desk,evidence,stage,genre):
    """Original graphics over inherited review footage; no new external assets."""
    if genre not in GENRES:raise ValueError('unknown genre')
    if desk.size!=(908,758) or evidence.size!=(908,758):raise ValueError('bad panel size')
    accent=PALETTES[genre]
    im=bg_frame(desk,accent)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((24,22,884,736),radius=34,fill=(5,17,31,214),outline=(*accent,235),width=3)
    d.rounded_rectangle((54,48,362,98),radius=15,fill=(*accent,240))
    d.text((208,73),['QUESTION / 01','EXAMPLE / 02','FIRST STEP / 03'][stage],font=font(25),anchor='mm',fill=(7,25,36,255))
    if stage==0:
        # Large emotional first-second hook, not a measured productivity claim.
        d.text((60,158),'その仕事、',font=font(77),fill=(255,255,255,255))
        d.text((60,265),'まだ手作業？',font=font(90),fill=(255,222,110,255),stroke_width=2,stroke_fill=(10,22,33,255))
        d.line((60,400,840,400),fill=(*accent,210),width=4)
        d.text((68,454),'同じ作業を毎日くり返すなら',font=font(38),fill=(227,242,246,255))
        d.rounded_rectangle((68,558,840,657),radius=22,fill=(11,77,93,230))
        d.text((454,607),'まず「何を減らすか」を決める',font=font(35),anchor='mm',fill=(255,255,255,255))
    elif stage==1:
        d.text((58,129),'具体例：表計算の確認',font=font(46),fill=(255,255,255,255))
        crop=fit_cover(evidence,786,410,zoom=1.0).convert('RGBA')
        im.alpha_composite(crop,(61,207))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((61,207,847,617),radius=13,outline=(*accent,255),width=6)
        d.rounded_rectangle((62,631,847,703),radius=14,fill=(10,35,51,250))
        d.text((454,667),'実演映像から再利用 / 架空データ',font=font(27),anchor='mm',fill=(230,242,245,255))
    elif stage==2:
        d.text((57,133),'最初に決めること',font=font(58),fill=(255,255,255,255))
        for i,(num,label,sub) in enumerate([('01','対象','毎日の作業を1つ選ぶ'),('02','目的','何を改善したいか決める'),('03','確認','結果を自分で確かめる')]):
            y=246+i*147
            d.rounded_rectangle((55,y,850,y+122),radius=20,fill=(11,39,59,245),outline=(*accent,225),width=3)
            d.rounded_rectangle((75,y+20,165,y+102),radius=19,fill=(*accent,255))
            d.text((120,y+61),num,font=font(38),anchor='mm',fill=(3,20,30,255))
            d.text((195,y+23),label,font=font(42),fill=(255,255,255,255))
            d.text((195,y+74),sub,font=font(28),fill=(198,226,235,255))
    else:raise ValueError('stage 0..2 required')
    return im.convert('RGB')

def stage_index(local,total):
    if not 0<=local<total or total<9:raise ValueError('invalid beat position')
    return min(2,3*local//total)

def eased(t):
    t=max(0.0,min(1.0,t));return t*t*(3-2*t)

def animate(panels,local,total):
    """4-frame crossfade at beat boundaries; avoids full-frame flash."""
    idx=stage_index(local,total)
    edges=[total//3,(2*total)//3]
    if idx>0:
        boundary=edges[idx-1]
        if local<boundary+4:
            alpha=eased((local-boundary+1)/4)
            return Image.blend(panels[idx-1],panels[idx],alpha)
    return panels[idx]

def render(source,output,manifest,genre='ai_work',window=WINDOW,desk_frame=20,evidence_frame=195):
    n=validate(source,output,manifest,genre,window,desk_frame,evidence_frame)
    desk=frame_crop(source,desk_frame);evidence=frame_crop(source,evidence_frame)
    panels=[panel_beat(desk,evidence,i,genre) for i in range(3)]
    cap=cv2.VideoCapture(str(source))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for i in range(n):
            ok,fr=cap.read()
            if not ok:raise RuntimeError('source frame truncated')
            if window[0]<=i<window[1]:
                panel=animate(panels,i-window[0],window[1]-window[0])
                x0,y0,x1,y1=PANEL
                fr[y0:y1,x0:x1]=cv2.cvtColor(np.asarray(panel),cv2.COLOR_RGB2BGR)
                changed+=1
            p.stdin.write(fr.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError('ffmpeg: '+err[-1500:])
    except Exception:
        p.kill();p.wait();Path(output).unlink(missing_ok=True);raise
    finally:cap.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=streams(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':raise RuntimeError('invalid output stream')
    return {'cycle':855,'genre':genre,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'frames':n,'changed_frames':changed,'window':list(window),'picture_beats':3,
            'full_av_decode':True,'independent_japanese_asr_verified':False,
            'semantic_subtitle_sync_verified':False,'source_rights_reviewed':False,
            'smartphone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):p.add_argument('--'+k,required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--window',nargs=2,type=int,default=list(WINDOW))
    p.add_argument('--desk-frame',type=int,default=20)
    p.add_argument('--evidence-frame',type=int,default=195)
    a=p.parse_args()
    r=render(a.source,a.output,json.loads(Path(a.manifest).read_text(encoding='utf-8')),
             a.genre,tuple(a.window),a.desk_frame,a.evidence_frame)
    Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))