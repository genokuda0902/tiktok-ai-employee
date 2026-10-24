#!/usr/bin/env python3
"""cycle808: speech-safe kinetic action-plan overlay. REVIEW ONLY, not approved."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
TOTAL_FRAMES=718
START_FRAME=445
SCENE_FRAMES=94
GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
ACCENTS={'ai_work':'#48B9F7','beauty':'#E99BCA','love_psychology':'#EF94AB',
         'money_saving':'#E6B961','sales_business':'#65E0CE','career':'#85BEF5',
         'health_life':'#8EDFA6','science':'#A4ABF6','travel_food':'#F1B77B',
         'product_life':'#8CD8D8'}
STEPS=(('誰が','担当を決める'),('何を','改善を１つ試す'),('いつまで','今日中に振り返る'))
EXPECTED_CAPTION='対策は、今日できる行動に変える。'
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf')

def font(size):
    path=os.getenv('CYCLE808_FONT') or next((p for p in FONTS if Path(p).is_file()),None)
    if not path: raise RuntimeError('Japanese font unavailable; set CYCLE808_FONT')
    return ImageFont.truetype(path,size)

def clamp(v):return max(0.,min(1.,v))
def ease(v):
    t=clamp(v)
    return 1-(1-t)**3

def validate(genre,steps):
    if genre not in GENRES: raise ValueError('Unsupported genre')
    if len(steps)!=3: raise ValueError('Exactly three action beats are required')
    for label,value in steps:
        if not isinstance(label,str) or not 1<=len(label)<=6:raise ValueError('Invalid label')
        if not isinstance(value,str) or not 1<=len(value)<=14:raise ValueError('Invalid value')
        if any(ch in label+value for ch in ('\n','\r','\x00')):raise ValueError('No multiline content')
        if ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),value,font=font(40))[2]>505:
            raise ValueError('Action value exceeds text safe width')

def action_frame(i,genre='sales_business',steps=STEPS):
    validate(genre,steps)
    if not 0<=i<SCENE_FRAMES:raise ValueError('Frame index out of bounds')
    accent=ACCENTS[genre]
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((130,742,950,1302),radius=34,
                        fill=(9,24,43,251),outline=(87,153,172,235),width=3)
    d.rounded_rectangle((157,762,923,852),radius=22,fill=(27,64,81,255))
    d.text((184,775),'TODAY  /  ACTION PLAN',font=font(34),fill=accent)
    d.text((744,785),'行動例',font=font(27),fill='#F4D48C')
    for j,(label,value) in enumerate(steps):
        t=ease((i-(6,33,60)[j])/13)
        if t<=0:continue
        y=871+j*120
        x=169+round((1-t)*125)
        alpha=round(246*t)
        d.rounded_rectangle((x,y,x+735,y+102),radius=21,
                            fill=(26,59,75,alpha),outline=(103,159,175,round(215*t)),width=2)
        d.ellipse((x+16,y+20,x+75,y+79),fill=(67,157,164,alpha))
        d.text((x+33,y+24),str(j+1),font=font(31),fill='#0C2434')
        d.text((x+94,y+16),label,font=font(29),fill='#A9D3DB')
        d.text((x+248,y+17),value,font=font(41),fill='#FFFFFF')
        if t>0.98:
            d.line((x+668,y+50,x+681,y+64),fill=accent,width=7)
            d.line((x+681,y+64,x+708,y+32),fill=accent,width=7)
    progress=ease((i-5)/78)
    d.rounded_rectangle((170,1252,910,1267),radius=7,fill=(48,82,95,255))
    if progress>0:
        d.rounded_rectangle((170,1252,170+round(740*progress),1267),radius=7,fill=accent)
    return im

def cmd(args):
    return subprocess.run(args,check=True,capture_output=True).stdout

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_entries',
       'format=duration:stream=codec_name,width,height,avg_frame_rate,nb_frames,sample_rate',
       '-of','json',str(path)]))

def audio_hash(path):
    return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',str(path),
       '-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def render(source,output,genre='sales_business',steps=STEPS):
    validate(genre,steps)
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    meta=probe(source)
    vs=next(s for s in meta['streams'] if s['codec_name']=='h264')
    aud=next(s for s in meta['streams'] if s['codec_name']=='aac')
    if (vs['width'],vs['height'],vs['avg_frame_rate'],int(vs['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):
        raise ValueError('Source geometry/timing differs from cycle807')
    if aud['sample_rate']!='48000':raise ValueError('Source must have 48kHz AAC')
    with tempfile.TemporaryDirectory() as tmp:
        frames=Path(tmp)
        for i in range(SCENE_FRAMES):
            action_frame(i,genre,steps).save(frames/f'action_{i:03d}.png')
        flt=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/({FPS}*TB)[ov];' \
            '[0:v][ov]overlay=x=0:y=0:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]'
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(frames/'action_%03d.png'),
             '-filter_complex',flt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p',
             '-r',str(FPS),'-frames:v',str(TOTAL_FRAMES),'-c:a','copy',
             '-movflags','+faststart',str(output)])
    cmd(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    new=probe(output)
    v=next(s for s in new['streams'] if s['codec_name']=='h264')
    a=next(s for s in new['streams'] if s['codec_name']=='aac')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):
        raise RuntimeError('Video metadata changed')
    if a['sample_rate']!='48000' or audio_hash(source)!=audio_hash(output):
        raise RuntimeError('Audio was modified')
    qa={'cycle':808,'source_cycle':807,'genre':genre,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'change':'3-stage kinetic action-plan demo; replaces static scene-6 card only',
        'changed_frames':[START_FRAME,START_FRAME+SCENE_FRAMES-1],
        'steps':[{'label':x,'action':y} for x,y in steps],
        'disclosure':'行動例 / example, not verified company performance',
        'source_caption_scene6':EXPECTED_CAPTION,'caption_voice_meaning':'NOT VERIFIED - no independent Japanese ASR',
        'caption_visibility':'SOURCE INHERITED - optical QA still required',
        'voice_naturalness':'NOT VERIFIED','voice_rights':'NOT VERIFIED',
        'smartphone_playback':'NOT VERIFIED','employee_approval':False,
        'video_frames':TOTAL_FRAMES,'duration_seconds':float(new['format']['duration']),
        'resolution':[W,H],'fps':FPS,'audio_sample_rate':48000,
        'audio_adts_sha256':audio_hash(output),'source_sha256':sha(source),'output_sha256':sha(output),
        'no_paid_services':True,'no_auto_post':True,'no_merge':True}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--genre',choices=GENRES,default='sales_business')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
