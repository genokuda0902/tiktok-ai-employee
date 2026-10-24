#!/usr/bin/env python3
"""Review-only, 10-genre opening-hook kinetic card. No media uploads or posting.

Reimplementation of the existing sales/business review: replaces only the flat
WHAT/WHY/HOW illustration during frames 0..89. It preserves existing captions
outside the overlay and stream-copies the inherited AAC voice without changes.
The generated private review video must never be published without approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, TOTAL = 1080, 1920, 30, 718
HOOK_FRAMES, CARD_W, CARD_H = 90, 850, 600
CARD_X, CARD_Y = 115, 730
PUBLICATION_APPROVED = False
AUTO_POST = False
STAGES = ('目的', '原因', '行動')
GENRE_ACCENTS = {
    'ai_work':'#55d6ff', 'beauty':'#ff99d4',
    'love_psychology':'#ff9cbb', 'money_saving':'#8fe7a2',
    'sales_business':'#60e6d2', 'career':'#a8b8ff',
    'health_life':'#93e2b2', 'science':'#9ecbff',
    'travel_food':'#ffcc83', 'product_life':'#a8d8ef',
}
FONT_CANDIDATES = (
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
)

def font(size):
    path = os.environ.get('CYCLE812_FONT') or next((p for p in FONT_CANDIDATES if Path(p).is_file()), None)
    if not path: raise RuntimeError('Japanese font missing; set CYCLE812_FONT')
    return ImageFont.truetype(path, size)

def validate(genre):
    if genre not in GENRE_ACCENTS: raise ValueError('Unsupported genre')
    if not (CARD_X >= 100 and CARD_X+CARD_W <= W-100):
        raise ValueError('Card outside horizontal safe area')
    if CARD_Y < 280 or CARD_Y+CARD_H > 1510:
        raise ValueError('Card outside caption-safe region')
    return GENRE_ACCENTS[genre]

def hex_rgb(color):
    return tuple(int(color[i:i+2],16) for i in (1,3,5))

def blend(a,b,t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

def draw_frame(frame, genre='sales_business'):
    if not 0 <= frame < HOOK_FRAMES: raise ValueError('Frame outside hook')
    accent = hex_rgb(validate(genre))
    im = Image.new('RGB',(CARD_W,CARD_H),'#071a2a')
    d = ImageDraw.Draw(im)
    # Fully opaque RGB card prevents inherited text ghosting.
    d.rounded_rectangle((6,6,844,594),radius=35,fill='#0b2538',outline=accent,width=3)
    # Low-cost moving light band; no licensed image asset or external API.
    sweep = (frame*12)%1100 - 160
    for dx in range(-52,53,13):
        x=sweep+dx
        if 35 < x < 815:
            k=max(0,1-abs(dx)/65)
            d.line([(x,35),(x-135,555)],fill=blend((14,44,64),accent,k*.24),width=4)
    d.text((43,34),'QUESTION  →  DECISION',font=font(34),fill='#f4fcff')
    d.text((45,94),'目的を決め、原因を見つけ、行動する。',font=font(30),fill='#b7d6e1')
    d.line((43,155,807,155),fill='#386879',width=3)
    # 3 beats within first 2.1 seconds: 0-0.7 / 0.7-1.4 / 1.4-2.1.
    active=min(2,frame//21)
    for j,(label,cx) in enumerate(zip(STAGES,(155,425,695))):
        is_active=j<=active
        if j==active:
            pulse=1+0.045*math.sin(frame*0.24)
        else:
            pulse=1
        radius=72*pulse
        edge=accent if is_active else (64,103,121)
        fill=(21,79,91) if is_active else (12,45,63)
        d.ellipse((cx-radius,216-radius,cx+radius,216+radius),fill=fill,outline=edge,width=6 if is_active else 3)
        d.text((cx-26,199),str(j+1).zfill(2),font=font(31),fill='#e5fcff' if is_active else '#7397a8')
        # labels do not overlap or move outside safe area
        bbox=d.textbbox((0,0),label,font=font(56))
        tw=bbox[2]-bbox[0]
        d.text((cx-tw/2,327),label,font=font(56),fill='#ffffff' if is_active else '#779eaf')
        if j<2:
            d.line((cx+91,216,cx+175,216),fill=accent if active>j else '#2c5a6e',width=8)
            d.polygon(((cx+175,202),(cx+198,216),(cx+175,230)),fill=accent if active>j else '#2c5a6e')
    # Animated beat progress, separate from existing top timeline/subtitles.
    d.rounded_rectangle((52,446,798,468),radius=10,fill='#22495d')
    progress=(frame+1)/HOOK_FRAMES
    d.rounded_rectangle((52,446,52+max(12,round(746*progress)),468),radius=10,fill=accent)
    d.text((55,504),'WHY  →  HOW',font=font(39),fill='#efffff')
    d.text((558,512),f'{active+1} / 3',font=font(31),fill=accent)
    return im

def run(command):
    p=subprocess.run(command,capture_output=True,text=True)
    if p.returncode: raise RuntimeError('command failed: '+ ' '.join(map(str,command))+'\n'+p.stderr[-2500:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def audio_hash(path):
    with tempfile.NamedTemporaryFile(suffix='.aac') as tmp:
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',tmp.name])
        return sha256(tmp.name)

def render(source,output,genre='sales_business',synthetic_source=False):
    validate(genre)
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle812_') as td:
        frames=Path(td)
        for i in range(HOOK_FRAMES):
            draw_frame(i,genre).save(frames/f'{i:03}.png')
        fg='[1:v]format=rgba,setpts=PTS-STARTPTS[card];[0:v][card]overlay=x=115:y=730:eof_action=pass:shortest=0:format=auto[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(frames/'%03d.png'),
             '-filter_complex',fg,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
             '-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',str(output)])
    p=probe(output)
    video=next(s for s in p['streams'] if s['codec_type']=='video')
    audio=next(s for s in p['streams'] if s['codec_type']=='audio')
    if (video['width'],video['height'],video['avg_frame_rate'])!=(W,H,'30/1'): raise RuntimeError('Bad video dimensions/fps')
    if int(video.get('nb_frames',0))!=TOTAL: raise RuntimeError('Bad frame count')
    if audio['codec_name']!='aac' or audio['sample_rate']!='48000': raise RuntimeError('Bad audio')
    if abs(float(p['format']['duration'])-TOTAL/FPS)>0.06: raise RuntimeError('Bad duration')
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(output),'-f','null','-'])
    before,after=audio_hash(source),audio_hash(output)
    if before!=after: raise RuntimeError('Inherited audio bitstream changed')
    qa={'cycle':812,'genre':genre,'frames':TOTAL,'fps':FPS,'width':W,'height':H,
        'duration_seconds':round(float(p['format']['duration']),6),
        'hook_frames':HOOK_FRAMES,'hook_duration_seconds':HOOK_FRAMES/FPS,
        'aac_bitstream_identical':True,'aac_adts_sha256':after,
        'synthetic_source':synthetic_source,'japanese_audio_inherited':not synthetic_source,
        'japanese_voice_semantics_verified':False,
        'caption_region_outside_overlay':True,'caption_semantics_verified':False,
        'full_av_decode_pass':True,'smartphone_verified':False,
        'rights_approved':False,'publication_approved':PUBLICATION_APPROVED,
        'auto_post':AUTO_POST,'private_review_only':True,'output_sha256':sha256(output)}
    (output.parent/'cycle812_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--genre',default='sales_business',choices=tuple(GENRE_ACCENTS))
    parser.add_argument('--synthetic-source',action='store_true',help='CI synthetic tone: not Japanese narration')
    args=parser.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.synthetic_source),ensure_ascii=False,indent=2))