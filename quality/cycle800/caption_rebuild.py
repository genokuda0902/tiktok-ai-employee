#!/usr/bin/env python3
"""cycle800: 10-genre high-contrast Japanese caption rebuild for review MP4.

Offline. Inherited audio copied without re-encoding. Original media rights remain
unverified; this is NOT a publication authorization or new TTS generator.
"""
import argparse, bisect, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAP_Y, CAP_H = 1510, 260
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work':'#B9A4FF', 'beauty':'#FFB9DF', 'love_psychology':'#D7B5FF',
    'money_saving':'#89EFCB', 'sales_business':'#7FD7FF', 'career':'#A4D8FF',
    'health_life':'#8AF0D1', 'science':'#43E5D0', 'travel_food':'#87E1F2',
    'product_life':'#D4B6FF'
}

def validate_cues(cues, frame_count):
    if not cues: raise ValueError('No captions')
    prev = -1
    for cue in cues:
        if set(cue) != {'start','end','text','accent'}: raise ValueError('Bad caption fields')
        if not (isinstance(cue['start'],int) and isinstance(cue['end'],int)
                and prev < cue['start'] < cue['end'] <= frame_count):
            raise ValueError('Invalid caption order or bounds')
        if not (isinstance(cue['text'],str) and cue['text'] and cue['accent'] in cue['text']):
            raise ValueError('Missing text/accent')
        prev = cue['end']-1
    return True

def contrast_ratio(a,b):
    def lum(color):
        v=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        v=[q/12.92 if q<=0.04045 else ((q+0.055)/1.055)**2.4 for q in v]
        return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]
    x,y=sorted((lum(a),lum(b)),reverse=True)
    return (x+0.05)/(y+0.05)

def make_caption(cue, genre):
    if genre not in GENRES: raise ValueError('Unknown genre')
    fg=GENRES[genre]
    im=Image.new('RGBA',(WIDTH,CAP_H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((37,10,1043,247),radius=29,fill='#031522',outline='#346070',width=3)
    d.rounded_rectangle((57,43,66,214),radius=4,fill=fg)
    text,accent=cue['text'],cue['accent']
    size=80
    while size>48:
        font=ImageFont.truetype(FONT,size)
        if d.textbbox((0,0),text,font=font)[2] <= 900: break
        size-=2
    full_w=d.textbbox((0,0),text,font=font)[2]
    x=(WIDTH-full_w)//2; y=67
    prefix, suffix=text.split(accent,1)
    w1=d.textbbox((0,0),prefix,font=font)[2] if prefix else 0
    w2=d.textbbox((0,0),accent,font=font)[2]
    for dx,dy in ((2,3),(0,3)):
        d.text((x+dx,y+dy),text,font=font,fill='#000C12',stroke_width=1)
    if prefix: d.text((x,y),prefix,font=font,fill='#FFFFFF')
    d.text((x+w1,y),accent,font=font,fill=fg)
    if suffix: d.text((x+w1+w2,y),suffix,font=font,fill='#FFFFFF')
    line_y=184
    d.rounded_rectangle((x+w1,line_y,x+w1+max(24,w2),line_y+7),radius=3,fill=fg)
    return np.asarray(im)

def apply_overlay(frame, overlay, opacity):
    if frame.shape[:2] != (HEIGHT,WIDTH): raise ValueError('Frame shape mismatch')
    out=frame[CAP_Y:CAP_Y+CAP_H,:,:]
    alpha=(overlay[:,:,3:4].astype(np.float32)/255.0)*(opacity/255.0)
    color=overlay[:,:,:3][:,:,::-1].astype(np.float32)
    out[:]=(out.astype(np.float32)*(1-alpha)+color*alpha).clip(0,255).astype('uint8')
    return frame

def render(source,target,cues,genre='science'):
    if genre not in GENRES:raise ValueError('Unknown genre')
    source=Path(source);target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('Source not open')
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (round(cap.get(3)),round(cap.get(4)))!=(WIDTH,HEIGHT) or abs(cap.get(5)-FPS)>0.1:
        raise ValueError('Expected 1080x1920, 30fps')
    validate_cues(cues,n)
    overlays=[make_caption(c,genre) for c in cues]
    blank=make_caption({'text':' ','accent':' '},genre)
    starts=[c['start'] for c in cues]
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0',
         '-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            i=bisect.bisect_right(starts,frames)-1
            if i>=0 and frames<cues[i]['end']:
                fade=min(1.,(frames-cues[i]['start']+1)/4,(cues[i]['end']-frames)/4)
                overlay=overlays[i];opacity=int(255*max(0.0,fade))
            else:
                overlay=blank;opacity=255
            proc.stdin.write(apply_overlay(frame,overlay,opacity).tobytes())
            frames+=1
    except Exception:
        proc.kill();raise
    finally:
        cap.release()
        if proc.stdin:proc.stdin.close()
    err=proc.stderr.read().decode('utf8','replace');code=proc.wait()
    if code:raise RuntimeError('ffmpeg error '+err[-500:])
    if frames!=n:raise RuntimeError(f'Frames changed {frames} != {n}')
    return {'frames':frames,'genre':genre,'output':str(target),'captions':len(cues)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--captions',required=True);p.add_argument('--genre',choices=list(GENRES),default='science')
    a=p.parse_args();c=json.loads(Path(a.captions).read_text(encoding='utf8'))
    print(json.dumps(render(a.source,a.output,c,a.genre),ensure_ascii=False))
