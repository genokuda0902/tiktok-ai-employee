"""cycle853: offline, rights-gated evidence-reveal from an EXISTING local video.

This is an original reimplementation. It never downloads or publishes media.
Scene 8 shows two genuine states from a fictional Writer interaction recorded
in scene 7; it makes NO claim about measured productivity or AI capability.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison_lifestyle')
PALETTES = {g: (36+(i*7)%43, 196-(i*5)%35, 208-(i*6)%37) for i,g in enumerate(GENRES)}
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'contains_personal_data': False,
          'fictional_gui_evidence': True}
PANEL = (86, 476, 994, 1234)
WINDOW = (588, 691)
EVIDENCE = (515, 575)  # frames in existing fictional Writer scene 7
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))


def av(path):
    ss=probe(path)['streams']
    return (next((s for s in ss if s['codec_type']=='video'),None),
            next((s for s in ss if s['codec_type']=='audio'),None))


def stage(local, total):
    if not isinstance(local,int) or not 0 <= local < total or total < 3:
        raise ValueError('invalid frame or window')
    return min(2, 3*local//total)


def validate(source, output, manifest, genre, window, evidence):
    source=Path(source); output=Path(output)
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError('missing input video')
    if manifest != {**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('manifest mismatch: fail closed')
    if output.exists() or source.resolve()==output.resolve():
        raise ValueError('overwrite forbidden')
    v,a=av(source)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name']) != ('h264',1080,1920,'30/1','aac'):
        raise ValueError('source must be 1080x1920 H264 30fps and AAC')
    n=int(v['nb_frames'])
    if len(window)!=2 or not all(type(x)==int for x in window) or not 0 <= window[0] < window[1] <= n:
        raise ValueError('bad scene window')
    if len(evidence)!=2 or not all(type(x)==int for x in evidence) or not 0 <= evidence[0] < evidence[1] < window[0]:
        raise ValueError('evidence must precede reveal scene')
    return n


def extract_evidence(source, evidence):
    cap=cv2.VideoCapture(str(source)); shots=[]
    try:
        for i in evidence:
            cap.set(cv2.CAP_PROP_POS_FRAMES,i)
            ok,fr=cap.read()
            if not ok:raise RuntimeError('evidence frame unavailable')
            x0,y0,x1,y1=PANEL
            # Crop only the original picture area, never headings/subtitles.
            shot=Image.fromarray(cv2.cvtColor(fr[y0+126:y0+612,x0+22:x1-22],cv2.COLOR_BGR2RGB))
            shots.append(shot)
    finally:cap.release()
    return shots


def render_panel(shots, local, total, genre):
    if len(shots)!=2:raise ValueError('two evidence frames required')
    s=stage(local,total);accent=PALETTES[genre]
    w,h=908,758
    yy=np.linspace(0,1,h,dtype=np.float32)[:,None,None]
    top=np.array([7,18,34],dtype=np.float32)[None,None,:]
    bottom=np.array([4,40,51],dtype=np.float32)[None,None,:]
    base=np.repeat((top*(1-yy)+bottom*yy).astype('uint8'),w,axis=1)
    im=Image.fromarray(base,'RGB');d=ImageDraw.Draw(im)
    ft=lambda size:ImageFont.truetype(FONT,size)
    d.rounded_rectangle((9,9,899,749),radius=25,outline=accent,width=4)
    d.text((40,42),'実際のWriter画面から',font=ft(34),fill=(230,249,252))
    d.text((866,59),'架空データ',font=ft(24),anchor='rm',fill=(164,222,232))
    d.rounded_rectangle((26,102,882,666),radius=22,fill=(7,26,42),outline=(37,89,106),width=2)
    # Large evidence frames in first two beats; side-by-side comparison in final beat.
    if s in (0,1):
        # Zoom into the real document text, not an invented result.
        original=shots[s]
        iw0,ih0=original.size
        shot=original.crop((int(iw0*.12),int(ih0*.12),int(iw0*.80),int(ih0*.88)))
        zoom=1.0+0.035*((local % max(1,total//3))/max(1,total//3))
        iw,ih=shot.size
        xpad=int((iw-iw/zoom)/2);ypad=int((ih-ih/zoom)/2)
        shot=shot.crop((xpad,ypad,iw-xpad,ih-ypad))
        shot=ImageOps.contain(shot,(808,428),Image.Resampling.LANCZOS)
        im.paste(shot,((w-shot.width)//2,183+(428-shot.height)//2))
        d=ImageDraw.Draw(im)
        label=('BEFORE  |  目的と条件を確認','AFTER  |  指示を整理・保存')[s]
        d.rounded_rectangle((58,116,850,170),radius=12,fill=(12,53,70))
        d.text((454,142),label,font=ft(31),anchor='mm',fill=(255,255,255))
    else:
        # A side-by-side proof of the SAME local Writer document, not a fake result.
        for j,shot in enumerate(shots):
            x=52+j*414
            d.rounded_rectangle((x,132,x+390,602),radius=15,fill=(236,241,245))
            display=ImageOps.contain(shot,(368,382),Image.Resampling.LANCZOS)
            im.paste(display,(x+(390-display.width)//2,195+(382-display.height)//2))
            d=ImageDraw.Draw(im)
            d.rounded_rectangle((x+8,143,x+382,189),radius=10,fill=(14,65,83))
            d.text((x+195,166),('BEFORE','AFTER')[j],font=ft(28),anchor='mm',fill=(255,255,255))
        d.text((454,621),'確認  →  テンプレート化',font=ft(29),anchor='mm',fill=(216,249,248))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((28,683,880,734),radius=14,fill=(10,62,73),outline=accent,width=2)
    d.text((454,709),('まず目的を明確に','使える形に整理','次回も使える状態へ')[s],font=ft(31),anchor='mm',fill=(255,255,255))
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)


def composite(frame,shots,local,total,genre):
    if frame.shape[:2]!=(1920,1080):raise ValueError('bad source frame')
    x0,y0,x1,y1=PANEL
    out=frame.copy()
    # Preserve original scene heading (<430) and Japanese subtitle region (>1234).
    # Remove any old picture title that extended above the picture inset.
    out[430:y0,x0:x1]=(5,18,30)
    out[y0:y1,x0:x1]=render_panel(shots,local,total,genre)
    return out


def render(source,output,manifest,genre='ai_work',window=WINDOW,evidence=EVIDENCE):
    source=Path(source);output=Path(output)
    n=validate(source,output,manifest,genre,window,evidence)
    shots=extract_evidence(source,evidence)
    inp=cv2.VideoCapture(str(source))
    proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
        '-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264',
        '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(output)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for idx in range(n):
            ok,fr=inp.read()
            if not ok:raise RuntimeError('input truncated')
            if window[0]<=idx<window[1]:
                fr=composite(fr,shots,idx-window[0],window[1]-window[0],genre);changed+=1
            proc.stdin.write(fr.tobytes())
        proc.stdin.close();err=proc.stderr.read().decode(errors='replace')
        if proc.wait():raise RuntimeError('ffmpeg failed: '+err[-1000:])
    except Exception:
        proc.kill();proc.wait();output.unlink(missing_ok=True);raise
    finally:inp.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=av(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':raise RuntimeError('output mismatch')
    return {'cycle':853,'source_sha256':sha256(source),'output_sha256':sha256(output),
        'genre':genre,'frames':n,'changed_frames':changed,'window':list(window),
        'evidence_frames':list(evidence),'beats':3,'full_av_decode':True,
        'source_rights_reviewed':False,'publication_approved':False,
        'independent_japanese_asr_verified':False,'semantic_subtitle_sync_verified':False,
        'smartphone_playback_verified':False,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','report'):p.add_argument('--'+k,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args();s=Path(a.source)
    result=render(s,a.output,{**POLICY,'source_sha256':sha256(s)},a.genre)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))