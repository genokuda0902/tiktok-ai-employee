#!/usr/bin/env python3
"""Cycle788 review-only 0–1.5s image-first BEFORE/AFTER hook. No publishing."""
import argparse
import json
import math
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_ALT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def ease(t):
    t=max(0.0,min(1.0,t))
    return t*t*(3-2*t)

def validate(cfg):
    if cfg.get('publication_approved') is not False or cfg.get('rights_reviewed') is not False:
        raise ValueError('REVIEW_ONLY: publication and rights cannot be asserted by renderer')
    if cfg.get('mode')!='review_only': raise ValueError('review_only mode required')
    duration=float(cfg['hook_seconds'])
    if not .8<=duration<=1.5: raise ValueError('hook_seconds must be 0.8..1.5')
    if tuple(cfg['canvas'])!=(W,H): raise ValueError('1080x1920 required')
    if not cfg['headline'] or len(cfg['headline'])>20: raise ValueError('headline must be short')
    if not cfg['subtitle'] or len(cfg['subtitle'])>35: raise ValueError('subtitle must be short')
    if len(cfg['before_label'])>12 or len(cfg['after_label'])>12: raise ValueError('labels too long')
    return True

def font(size,bold=True):
    return ImageFont.truetype(FONT if bold else FONT_ALT,size)

def cover_crop(im,box):
    x1,y1,x2,y2=box
    if not (0<=x1<x2<=im.width and 0<=y1<y2<=im.height): raise ValueError('bad crop')
    return im.crop((x1,y1,x2,y2))

def fit_cover(im,sz):
    tw,th=sz; iw,ih=im.size
    scale=max(tw/iw,th/ih)
    im=im.resize((math.ceil(iw*scale),math.ceil(ih*scale)),Image.Resampling.LANCZOS)
    x=(im.width-tw)//2; y=(im.height-th)//2
    return im.crop((x,y,x+tw,y+th))

@lru_cache(maxsize=1)
def make_bg():
    im=Image.new('RGB',(W,H))
    px=im.load()
    for y in range(H):
        for x in range(W):
            v=max(0,1-math.hypot((x-540)/1050,(y-960)/1600))
            px[x,y]=(int(5+7*v),int(19+24*v),int(38+42*v))
    d=ImageDraw.Draw(im,'RGBA')
    for x in range(0,W,108): d.line((x,250,x,1500),fill=(65,153,185,23),width=1)
    for y in range(250,1510,105): d.line((0,y,W,y),fill=(65,153,185,23),width=1)
    return im

def draw_card(canvas,photo,rect,label,accent,progress):
    x1,y1,x2,y2=rect; width=x2-x1; height=y2-y1
    offset=int((1-ease(progress))*140)
    x1+=(-offset if label=='BEFORE' else offset)
    x2+=(-offset if label=='BEFORE' else offset)
    if progress<=0: return
    shadow=Image.new('RGBA',(W,H)); sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1-8,y1-8,x2+8,y2+8),radius=32,fill=(*accent,45))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(28)))
    pic=fit_cover(photo,(width,height))
    mask=Image.new('L',(width,height))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,width,height),radius=27,fill=255)
    canvas.paste(pic,(x1,y1),mask)
    d=ImageDraw.Draw(canvas,'RGBA')
    d.rounded_rectangle((x1,y1,x2,y2),radius=27,outline=(*accent,245),width=5)
    d.rounded_rectangle((x1+15,y1+16,x1+width-15,y1+95),radius=18,fill=(3,16,29,225))
    d.text((x1+30,y1+20),label,font=font(40),fill=(*accent,255))

def make_frame(cfg,before,after,t):
    validate(cfg)
    dur=float(cfg['hook_seconds'])
    canvas=make_bg().convert('RGBA')
    d=ImageDraw.Draw(canvas,'RGBA')
    d.rounded_rectangle((80,252,500,310),radius=18,fill=(15,58,77,255),outline=(69,221,226,150),width=2)
    d.text((106,258),'AI × EXCEL  /  DEMO',font=font(29),fill=(173,246,245,255))
    for i,line in enumerate(cfg['headline'].split('\n')):
        d.text((92,360+i*108),line,font=font(83),fill=(255,255,255,255),stroke_width=2,stroke_fill=(3,19,35,255))
    d.text((94,603),cfg['subtitle'],font=font(37,False),fill=(138,243,238,255))
    bprog=ease(t/.45); aprog=ease((t-.22)/.50)
    draw_card(canvas,before,(80,755,515,1330),cfg['before_label'],(255,178,139),bprog)
    draw_card(canvas,after,(565,755,1000,1330),cfg['after_label'],(70,231,226),aprog)
    d=ImageDraw.Draw(canvas,'RGBA')
    if t>.65:
        a=int(255*ease((t-.65)/.32))
        d.ellipse((505,1032,575,1102),fill=(14,38,58,a),outline=(210,251,247,a),width=3)
        d.line([(523,1068),(556,1068)],fill=(247,250,230,a),width=5)
        d.polygon([(550,1055),(568,1068),(550,1081)],fill=(247,250,230,a))
    d.rounded_rectangle((80,1370,1000,1465),radius=21,fill=(5,21,34,255),outline=(70,155,177,140),width=2)
    d.text((113,1392),cfg['disclosure'],font=font(30,False),fill=(217,237,239,255))
    fade=1-ease((t-(dur-.18))/.18)
    canvas.putalpha(int(255*fade))
    return canvas

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def run(input_video,before_path,after_path,output,cfg,report):
    validate(cfg)
    input_video=Path(input_video); output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    info=probe(input_video)
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    if (video['width'],video['height'])!=(W,H): raise ValueError('bad source dimensions')
    if not any(s['codec_type']=='audio' for s in info['streams']): raise ValueError('narration track required')
    before=cover_crop(Image.open(before_path).convert('RGB'),cfg['before_crop'])
    after=cover_crop(Image.open(after_path).convert('RGB'),cfg['after_crop'])
    n=math.ceil(cfg['hook_seconds']*FPS)
    with tempfile.TemporaryDirectory(prefix='cycle788_') as td:
        p=Path(td)
        for i in range(n): make_frame(cfg,before,after,i/FPS).save(p/f'overlay_{i:04d}.png')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(input_video),
             '-framerate',str(FPS),'-i',str(p/'overlay_%04d.png'),
             '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
             '-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True)
    dst=probe(output)
    result={'input':str(input_video),'output':str(output),'hook_seconds':cfg['hook_seconds'],
            'frames_modified':n,'resolution':[W,H],'duration':float(dst['format']['duration']),
            'audio':'stream copy from review-only input','voice_caption_semantics':'NOT_VERIFIED',
            'rights_reviewed':False,'publication_approved':False,'review_status':'HUMAN_REVIEW',
            'reference_v33_direct_comparison':'NOT_AVAILABLE'}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True);ap.add_argument('--before',required=True)
    ap.add_argument('--after',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--config',required=True);ap.add_argument('--report',required=True)
    a=ap.parse_args()
    print(json.dumps(run(a.input,a.before,a.after,a.output,json.loads(Path(a.config).read_text(encoding='utf-8')),a.report),ensure_ascii=False))
