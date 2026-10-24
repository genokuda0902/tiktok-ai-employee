#!/usr/bin/env python3
"""cycle809: rights-safe *simulated* goal-entry UI motion for 10 genres.

No external images, private metrics, logos or actual service screen recordings.
Review only. Requires an existing approved-for-private-review source MP4.
"""
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
START_FRAME=90
SCENE_FRAMES=89
# Synthetic, non-company data. 10-genre contract is common, not 10 rendered videos.
SCENARIOS={
 'ai_work':('作業時間','10 分','#4ABFF6'),
 'beauty':('お手入れ','週 3 回','#EFA6C7'),
 'love_psychology':('対話時間','15 分','#F4A7BA'),
 'money_saving':('貯金目標','1 万円','#F1C56C'),
 'sales_business':('月間成約','20 件','#61DFCE'),
 'career':('学習時間','30 分','#91C3F3'),
 'health_life':('歩数目標','6000 歩','#9ADFB2'),
 'science':('実験回数','3 回','#B0B3F7'),
 'travel_food':('旅行予算','3 万円','#F6BE86'),
 'product_life':('片付け時間','15 分','#96DCD5'),
}
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf')

def font(size):
    path=os.getenv('CYCLE809_FONT') or next((p for p in FONTS if Path(p).is_file()),None)
    if not path:raise RuntimeError('Japanese font missing: set CYCLE809_FONT')
    return ImageFont.truetype(path,size)

def clamp(v):return max(0.,min(1.,v))
def ease(v):
    t=clamp(v)
    return 1-(1-t)**3

def validate(genre):
    if genre not in SCENARIOS:raise ValueError('Unsupported genre')
    metric,value,_=SCENARIOS[genre]
    d=ImageDraw.Draw(Image.new('RGB',(1,1)))
    if any(ch in metric+value for ch in ('\n','\r','\x00')):raise ValueError('No multiline')
    if d.textbbox((0,0),metric,font=font(36))[2]>350:raise ValueError('Metric too long')
    if d.textbbox((0,0),value,font=font(54))[2]>460:raise ValueError('Value too long')

def frame(i,genre='sales_business'):
    validate(genre)
    if not 0<=i<SCENE_FRAMES:raise ValueError('Frame outside scene')
    metric,value,accent=SCENARIOS[genre]
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
    # Source slide headline and lower spoken-Japanese caption remain visible.
    # Only the middle card x=118..962 y=788..1260 is covered.
    x0,y0,x1,y1=118,788,962,1260
    # Animate the whole synthetic UI entrance over 0.25 s.
    a=round(255*ease(i/8))
    d.rounded_rectangle((x0+9,y0+13,x1+9,y1+13),radius=30,fill=(0,8,20,round(115*a/255)))
    d.rounded_rectangle((x0,y0,x1,y1),radius=30,fill=(13,33,54,a),outline=(77,138,158,a),width=3)
    d.rounded_rectangle((x0+3,y0+3,x1-3,y0+82),radius=27,fill=(25,53,72,a))
    d.rectangle((x0+3,y0+56,x1-3,y0+82),fill=(25,53,72,a))
    for j,c in enumerate(((243,116,112,a),(240,191,99,a),(99,214,155,a))):
        cx=x0+34+j*34;cy=y0+41
        d.ellipse((cx-9,cy-9,cx+9,cy+9),fill=c)
    d.text((x0+157,y0+17),'GOAL / DEMO',font=font(33),fill=(235,247,251,a))
    d.text((x1-176,y0+23),'架空UI',font=font(25),fill=(250,213,133,a))
    d.text((x0+52,y0+104),'目標を入力',font=font(33),fill=(189,223,231,a))
    d.rounded_rectangle((x0+49,y0+159,x1-49,y0+265),radius=16,fill=(5,19,34,a),outline=(87,132,154,a),width=3)
    d.text((x0+72,y0+175),metric,font=font(34),fill=(172,210,222,a))
    # Typing takes ~1.0 s and deliberately pauses before a simulated click.
    chars=round(len(value)*ease((i-10)/34))
    typed=value[:chars]
    d.text((x0+354,y0+174),typed,font=font(52),fill=(255,255,255,a))
    if 10<=i<56 and (i//8)%2==0:
        tw=d.textbbox((0,0),typed,font=font(52))[2]
        px=min(x0+354+tw+9,x1-75)
        d.rectangle((px,y0+186,px+4,y0+242),fill=(255,255,255,a))
    clicked=i>=62
    by0=y0+289;by1=y0+363
    d.rounded_rectangle((x0+50,by0,x1-50,by1),radius=17,
                        fill=(39,127,122,a) if clicked else (33,92,106,a),
                        outline=(102,231,213,a),width=3)
    btn='✓  保存しました' if clicked else '目標を設定する'
    bx=(W-d.textbbox((0,0),btn,font=font(34))[2])//2
    d.text((bx,by0+13),btn,font=font(34),fill=(255,255,255,a))
    if 43<=i<70:
        # Moving simulated cursor, never pretending to be a real screen recording.
        t=ease((i-43)/24)
        cx=round(810+(610-810)*t);cy=round(931+(1030-931)*t)
        d.polygon([(cx,cy),(cx,cy+40),(cx+11,cy+29),(cx+24,cy+47),(cx+34,cy+41),(cx+20,cy+23),(cx+42,cy+20)],
                  fill=(247,252,255,a))
    d.text((x0+50,y0+378),'架空データ・操作イメージ',font=font(25),fill=(183,206,219,a))
    return im

def run(args):return subprocess.run(args,check=True,capture_output=True).stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_name,width,height,avg_frame_rate,nb_frames,sample_rate',
        '-of','json',str(path)]))

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def render(source,output,genre='sales_business'):
    validate(genre)
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    meta=probe(source)
    v=next(s for s in meta['streams'] if s['codec_name']=='h264')
    a=next(s for s in meta['streams'] if s['codec_name']=='aac')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):
        raise ValueError('Unexpected source video geometry/timing')
    if a['sample_rate']!='48000':raise ValueError('Expected 48 kHz AAC source')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for i in range(SCENE_FRAMES):frame(i,genre).save(p/f'overlay_{i:03d}.png')
        flt=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/({FPS}*TB)[ov];'
             '[0:v][ov]overlay=x=0:y=0:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(p/'overlay_%03d.png'),
             '-filter_complex',flt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p',
             '-r',str(FPS),'-frames:v',str(TOTAL_FRAMES),'-c:a','copy',
             '-movflags','+faststart',str(output)])
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    new=probe(output);v2=next(s for s in new['streams'] if s['codec_name']=='h264')
    a2=next(s for s in new['streams'] if s['codec_name']=='aac')
    if (v2['width'],v2['height'],v2['avg_frame_rate'],int(v2['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):
        raise RuntimeError('Unexpected output geometry/timing')
    if a2['sample_rate']!='48000' or audio_sha(source)!=audio_sha(output):
        raise RuntimeError('Original audio was modified')
    qa={'cycle':809,'source_cycle':808,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'change':'Simulated typing, cursor and save feedback in scene 2; replaces static goal card',
        'genre':genre,'genre_contract_count':len(SCENARIOS),
        'changed_frames':[START_FRAME,START_FRAME+SCENE_FRAMES-1],
        'synthetic_ui':True,'actual_app_recording':False,'fictional_data':True,
        'source_sha256':sha(source),'output_sha256':sha(output),'audio_adts_sha256':audio_sha(output),
        'duration_seconds':float(new['format']['duration']),'resolution':[W,H],
        'fps':FPS,'frames':TOTAL_FRAMES,'audio_sample_rate':48000,
        'speech_content_verified':False,'caption_semantic_sync_verified':False,
        'speech_naturalness_verified':False,'asset_rights_verified':False,
        'smartphone_verified':False,'reference_v33_compared':False,'employee_approved':False,
        'posting_allowed':False,'auto_post':False,'no_paid_services':True}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--genre',default='sales_business',choices=SCENARIOS)
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
