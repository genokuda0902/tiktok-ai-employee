#!/usr/bin/env python3
"""cycle807: animated, explicitly fictional KPI evidence panel, review only.

Uses a prior unapproved review MP4; does not synthesize/alter speech, post,
fetch private media, or claim that illustrated KPI numbers are actual results.
The 10 genre palette contract is reusable; only sales_business is rendered.
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

W,H,FPS=1080,1920,30
GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
COLORS={'ai_work':'#48B9F7','beauty':'#E99BCA','love_psychology':'#EF94AB',
        'money_saving':'#E6B961','sales_business':'#65E0CE','career':'#85BEF5',
        'health_life':'#8EDFA6','science':'#A4ABF6','travel_food':'#F1B77B',
        'product_life':'#8CD8D8'}
# All figures are illustrative, never business results.
DEMO=(('接続率',18,25),('成約率',12,20),('継続率',68,80))
START_FRAME=179  # after 94+85 frames of cycle806
SCENE_FRAMES=84
FONT_PATHS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf')

def get_font(size):
    path=os.getenv('CYCLE807_FONT') or next((p for p in FONT_PATHS if Path(p).exists()),None)
    if not path:raise RuntimeError('Japanese Noto font missing; set CYCLE807_FONT')
    return ImageFont.truetype(path,size)

def smoothstep(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)

def validate_demo(rows=DEMO):
    if len(rows)<1 or len(rows)>4:raise ValueError('Need 1..4 KPIs')
    for label,current,target in rows:
        if not isinstance(label,str) or not label or len(label)>8:raise ValueError('Invalid KPI label')
        if not all(isinstance(x,int) and 0<=x<=100 for x in (current,target)):
            raise ValueError('KPI values must be 0..100 integers')
        if target==0:raise ValueError('Target cannot be zero')

def panel_frame(index,genre='sales_business',rows=DEMO):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if not 0<=index<SCENE_FRAMES:raise ValueError('Frame out of bounds')
    validate_demo(rows)
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
    accent=COLORS[genre]
    d.rounded_rectangle((142,791,938,1292),radius=28,
                        fill=(18,46,64,252),outline=(112,190,203,230),width=3)
    d.text((198,826),'KPI  /  現状と目標',font=get_font(43),fill='#F4F9FF')
    d.text((730,835),'表示例',font=get_font(31),fill='#F6D488')
    # Fixed axes and labels, animation affects bars only.
    for j,(label,current,target) in enumerate(rows):
        y=923+j*104
        d.text((205,y-1),label,font=get_font(39),fill='#F4F9FF')
        d.rounded_rectangle((440,y+50,827,y+72),radius=10,fill=(60,83,103,255))
        goal_x=440+round(387*target/100)
        d.line((goal_x,y+43,goal_x,y+81),fill='#F6D488',width=5)
        # Stagger each bar to reveal an actual comparison rather than static decoration.
        progress=smoothstep((index/FPS-j*0.25)/1.15)
        filled=round(387*current/100*progress)
        if filled>=6:
            d.rounded_rectangle((440,y+50,440+filled,y+72),radius=10,fill=accent)
        if progress>0.18:
            d.text((653,y-3),f'{current}% / {target}%',font=get_font(32),fill='#FFFFFF')
    d.text((202,1250),'■ 現状     │ 目標   ※架空データ',font=get_font(27),fill='#C3DCE6')
    return im

def run(args):
    return subprocess.run(args,check=True,capture_output=True).stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_name,width,height,avg_frame_rate,nb_frames,sample_rate',
        '-of','json',str(path)]))

def aac_digest(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),
        '-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def render(source,output,genre='sales_business',work=None):
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if genre not in GENRES:raise ValueError('Unsupported genre')
    before=probe(source)
    vs=next(x for x in before['streams'] if x['codec_name']=='h264')
    au=next(x for x in before['streams'] if x['codec_name']=='aac')
    if (vs['width'],vs['height'],vs['avg_frame_rate'])!=(W,H,'30/1') or int(vs['nb_frames'])!=718:
        raise ValueError('Unexpected cycle806 source: expected 718 frames 1080x1920/30')
    if au['sample_rate']!='48000':raise ValueError('Unexpected source audio')
    with tempfile.TemporaryDirectory(dir=work) as tmp:
        frames=Path(tmp)
        for i in range(SCENE_FRAMES):
            panel_frame(i,genre).save(frames/f'panel_{i:03d}.png')
        overlay=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/({FPS}*TB)[ov];' \
                '[0:v][ov]overlay=x=0:y=0:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(frames/'panel_%03d.png'),
             '-filter_complex',overlay,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','22',
             '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v','718',
             '-c:a','copy','-movflags','+faststart',str(output)])
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    after=probe(output);outv=next(x for x in after['streams'] if x['codec_name']=='h264')
    if int(outv['nb_frames'])!=718 or (outv['width'],outv['height'])!=(W,H):
        raise RuntimeError('Output video metadata mismatch')
    if aac_digest(source)!=aac_digest(output):raise RuntimeError('Japanese AAC packets changed')
    qa={'cycle':807,'source_cycle':806,'genre':genre,'change':'animated fictional current-vs-target KPI evidence panel',
        'changed_frames':[START_FRAME,START_FRAME+SCENE_FRAMES-1],
        'demo_values':[{'metric':n,'current':c,'target':t} for n,c,t in DEMO],
        'disclaimer':'架空データ / illustrative, not actual performance',
        'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'voice_rights':'NOT VERIFIED','independent_japanese_asr':'NOT PERFORMED',
        'caption_voice_meaning':'NOT VERIFIED','smartphone_playback':'NOT VERIFIED',
        'audio_packet_sha256':aac_digest(output),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'duration_seconds':float(after['format']['duration']),'video_frames':718,
        'resolution':[W,H],'no_auto_post':True,'no_external_assets':True}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True)
    p.add_argument('--output',required=True);p.add_argument('--genre',choices=GENRES,default='sales_business')
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
