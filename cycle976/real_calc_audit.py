#!/usr/bin/env python3
"""Review-only: replace a fictional arithmetic audit card with real Calc-export evidence.
No uploads, no publication, no proprietary media included in source control.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
SAFE_BOTTOM=1240
START=14.5
SCENE_FRAMES=87
GENRES=('ai_work','finance','learning','health','travel','food','science','history','business','lifestyle')
PALETTES={'ai_work':'#43e0ce','finance':'#e7b65e','learning':'#65b7e5','health':'#67d4a3','travel':'#f1ad73','food':'#e7ad75','science':'#9e95e8','history':'#c5a978','business':'#6dc6df','lifestyle':'#e3a0d2'}
FONT_PATHS=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']

def font(size):
    for p in FONT_PATHS:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    raise RuntimeError('Japanese Noto CJK font required')

def check_genre(genre, synthetic):
    if genre not in GENRES: raise ValueError('Unknown genre; fail closed')
    if genre!='ai_work' and not synthetic: raise ValueError('Genre layout not reviewed; fail closed')

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def color(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))

def make_frame(proof, index, genre='ai_work', synthetic=False):
    check_genre(genre,synthetic)
    if not 0<=index<SCENE_FRAMES:raise ValueError('Frame outside scene')
    progress=index/(SCENE_FRAMES-1)
    stage=0 if index<23 else 1 if index<59 else 2
    im=Image.new('RGBA',(W,SAFE_BOTTOM),(5,20,37,255))
    d=ImageDraw.Draw(im)
    accent=color(PALETTES[genre]); white=(242,250,252,255)
    d.rounded_rectangle((38,36,1042,118),radius=25,fill=(8,39,60,255),outline=(*accent,230),width=3)
    d.text((68,58),'AI仕事術 / REAL CALC AUDIT',font=font(32),fill=white)
    d.text((58,172),'仮の数値を、実データで検算',font=font(51),fill=white)
    d.text((60,251),'架空データをCalcで計算した結果',font=font(29),fill=(163,220,225,255))
    for j,txt in enumerate(('01 仮の下書き','02 Calc検算','03 数値修正')):
        x=55+j*336
        active=j==stage
        d.rounded_rectangle((x,320,x+312,391),radius=19,fill=(*accent,245) if active else (24,62,78,255))
        d.text((x+14,336),txt,font=font(25),fill=(4,30,38,255) if active else (174,214,224,255))
    if stage==0:
        d.rounded_rectangle((70,445,1010,1000),radius=38,fill=(12,37,57,255),outline=(235,104,110,255),width=5)
        d.text((120,490),'AIの仮の下書き（未確認）',font=font(39),fill=white)
        d.text((390,598),'45',font=font(164),fill=(252,141,145,255))
        d.line((372,780,685,780),fill=(246,109,118,255),width=10)
        d.text((245,840),'そのまま使わない',font=font(50),fill=white)
    elif stage==1:
        d.rounded_rectangle((62,423,1018,1075),radius=33,fill=(225,240,242,255),outline=(*accent,255),width=6)
        crop=proof.crop((70,76,870,525))
        zoom=1+0.06*((index-23)/36)
        scaled=crop.resize((int(860*zoom),int(530*zoom)),Image.Resampling.LANCZOS)
        sx=(W-scaled.width)//2;sy=460-(scaled.height-530)//2
        im.paste(scaled,(sx,sy))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((195,1000,888,1092),radius=20,fill=(9,74,75,250))
        d.text((218,1019),'SUM：12＋16＋18＝46',font=font(42),fill=white)
    else:
        d.rounded_rectangle((66,435,1014,1025),radius=38,fill=(13,47,60,255),outline=(*accent,255),width=5)
        d.text((130,488),'CalcのSUMで検算完了',font=font(46),fill=white)
        d.text((125,620),'45',font=font(113),fill=(241,128,132,255))
        d.line((115,714,323,714),fill=(241,128,132,255),width=9)
        d.text((380,660),'→',font=font(91),fill=white)
        d.text((605,620),'46',font=font(113),fill=(*accent,255))
        d.rounded_rectangle((155,820,925,929),radius=23,fill=(21,93,90,255))
        d.text((190,845),'営業Bの合計も 29 と確認',font=font(39),fill=white)
    d=ImageDraw.Draw(im)
    d.text((58,1115),'実績ではありません｜社員確認後のみ手動投稿',font=font(28),fill=(213,230,235,255))
    d.rounded_rectangle((60,1177,1020,1194),radius=8,fill=(32,76,93,255))
    d.rounded_rectangle((60,1177,60+int(960*progress),1194),radius=8,fill=(*accent,255))
    if im.getbbox()[3]>SAFE_BOTTOM:raise RuntimeError('Caption safe region violation')
    return im

def render(source,proof,output,frames_dir,genre='ai_work',synthetic=False):
    check_genre(genre,synthetic)
    source,proof,output,frames_dir=map(Path,(source,proof,output,frames_dir))
    if not source.is_file() or not proof.is_file():raise FileNotFoundError('Source video or Calc proof missing')
    frames_dir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    p=Image.open(proof).convert('RGB')
    for i in range(SCENE_FRAMES):
        make_frame(p,i,genre,synthetic).save(frames_dir/f'frame_{i:03d}.png',optimize=True)
    fc=f"[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/TB[ov];[0:v][ov]overlay=x=0:y=0:enable='between(t,{START},{START+SCENE_FRAMES/FPS-1e-5})':eof_action=pass:format=auto[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(frames_dir/'frame_%03d.png'),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-frames:v','691','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'input_sha256':sha(source),'output_sha256':sha(output),'scene_start':START,'scene_frames':SCENE_FRAMES,'caption_safe_y':SAFE_BOTTOM,'genre':genre,'publication_approved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--proof',required=True);ap.add_argument('--output',required=True);ap.add_argument('--frames-dir',required=True);ap.add_argument('--genre',default='ai_work');ap.add_argument('--synthetic',action='store_true')
    a=ap.parse_args();print(json.dumps(render(a.source,a.proof,a.output,a.frames_dir,a.genre,a.synthetic),ensure_ascii=False,indent=2))
