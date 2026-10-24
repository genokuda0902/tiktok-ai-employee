#!/usr/bin/env python3
"""cycle810: reusable fictional-result animation, private-review only.

Source media must be approved for PRIVATE REVIEW; it is never uploaded to CI.
CI uses a wholly synthetic color+tone input. No claims of real sales results.
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
START_FRAME=628
SCENE_FRAMES=90
# Shared ten-genre design contract; all figures are fictional examples.
EXAMPLES={
 'ai_work': ('処理件数',8,20,'件','#60E6D1'),
 'beauty': ('練習回数',8,20,'回','#F2A9C8'),
 'love_psychology': ('対話時間',8,20,'分','#F4A8BC'),
 'money_saving': ('積立額',8,20,'千円','#F7CE79'),
 'sales_business': ('成約件数',8,20,'件','#60E6D1'),
 'career': ('学習回数',8,20,'回','#9EC8F4'),
 'health_life': ('運動時間',8,20,'分','#9CE7C0'),
 'science': ('観測回数',8,20,'回','#B4B8FF'),
 'travel_food': ('訪問件数',8,20,'件','#F7C18A'),
 'product_life': ('整理件数',8,20,'件','#9AE2DA'),
}
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc')

def font(size):
    p=os.getenv('CYCLE810_FONT') or next((v for v in FONTS if Path(v).is_file()),None)
    if not p: raise RuntimeError('Japanese font missing; set CYCLE810_FONT')
    return ImageFont.truetype(p,size)

def ease(x):
    x=max(0.,min(1.,x))
    return x*x*(3-2*x)

def check(genre):
    if genre not in EXAMPLES: raise ValueError('Unknown genre')
    metric,old,new,unit,_=EXAMPLES[genre]
    if not 0<old<new<=100: raise ValueError('Example must grow safely')
    if any(ch in metric+unit for ch in '\n\r\x00'): raise ValueError('Unsafe label')
    d=ImageDraw.Draw(Image.new('RGB',(1,1)))
    if d.textbbox((0,0),metric,font=font(39))[2]>380: raise ValueError('Label too long')
    return EXAMPLES[genre]

def text_center(d,y,s,size,color):
    f=font(size);box=d.textbbox((0,0),s,font=f)
    d.text(((W-(box[2]-box[0]))//2,y),s,font=f,fill=color)

def frame(i,genre='sales_business'):
    if not 0<=i<SCENE_FRAMES: raise ValueError('Frame outside scene')
    metric,old,new,unit,accent=check(genre)
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
    # Original headline (above 630) and narration caption (below 1370) remain.
    d.rounded_rectangle((112,680,968,1340),radius=40,fill=(10,31,49,253),outline=(95,166,186,255),width=4)
    d.rounded_rectangle((132,704,948,786),radius=27,fill=(28,68,86,255))
    text_center(d,713,f'{metric}の変化',45,(242,250,255,255))
    d.rounded_rectangle((774,718,939,768),radius=14,fill=(75,61,39,255))
    d.text((789,724),'架空の例',font=font(28),fill=(255,219,157,255))
    # Two bars. Grow the current bar after the first 0.4 seconds.
    bottom=1137
    old_h=146
    new_h=round((old_h*new/old)*ease((i-12)/40))
    d.rounded_rectangle((268,bottom-old_h,405,bottom),radius=18,fill=(125,155,174,255))
    if new_h>20:
        d.rounded_rectangle((660,bottom-new_h,798,bottom),radius=18,fill=(79,221,198,255))
    d.line((193,bottom+7,868,bottom+7),fill=(139,180,192,255),width=4)
    d.text((255,1149),'先週',font=font(38),fill=(222,232,241,255))
    d.text((650,1149),'今週',font=font(38),fill=(223,250,246,255))
    d.text((254,bottom-old_h-67),f'{old}{unit}',font=font(51),fill=(247,248,251,255))
    if i>=16:
        d.text((642,max(856,bottom-new_h-70)),f'{new}{unit}',font=font(55),fill=(255,255,255,255))
    # Opaque shapes avoid revealing source labels under translucent overlays.
    if i>=53:
        a=255
        d.line([(475,1022),(567,925)],fill=(255,202,93,a),width=15)
        d.polygon([(570,916),(533,927),(566,954)],fill=(255,202,93,a))
    if i>=68:
        a=255
        d.rounded_rectangle((417,1186,666,1266),radius=18,fill=(242,198,84,a))
        d.text((448,1194),'+150%',font=font(50),fill=(28,39,49,a))
    return im

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=False)
    if p.returncode: raise RuntimeError('Command failed: '+ ' '.join(map(str,cmd))+'\n'+p.stderr.decode(errors='replace')[-2000:])
    return p.stdout

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(p):
    return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate,nb_frames,sample_rate','-of','json',str(p)]))
def audio_hash(p):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def render(source,output,genre='sales_business'):
    check(genre)
    source=Path(source);output=Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    meta=probe(source)
    video=next((s for s in meta['streams'] if s['codec_name']=='h264'),None)
    audio=next((s for s in meta['streams'] if s['codec_name']=='aac'),None)
    if not video or (video['width'],video['height'],video['avg_frame_rate'],int(video['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):
        raise ValueError('Unexpected source video geometry or timing')
    if not audio or audio['sample_rate']!='48000':raise ValueError('Expected 48kHz AAC audio')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for i in range(SCENE_FRAMES):frame(i,genre).save(p/f'overlay_{i:03d}.png')
        flt=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/({FPS}*TB)[ov];'
             '[0:v][ov]overlay=x=0:y=0:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(p/'overlay_%03d.png'),
             '-filter_complex',flt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p',
             '-r',str(FPS),'-frames:v',str(TOTAL_FRAMES),'-c:a','copy','-movflags','+faststart',str(output)])
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    final=probe(output);v=next(s for s in final['streams'] if s['codec_name']=='h264')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL_FRAMES):raise RuntimeError('Bad output geometry')
    if audio_hash(source)!=audio_hash(output):raise RuntimeError('Inherited audio modified')
    qa={'cycle':810,'source_cycle':809,'genre':genre,'genre_contract_count':len(EXAMPLES),
        'changed_frames':[START_FRAME,START_FRAME+SCENE_FRAMES-1],
        'improvement':'Replace static final bars with timed fictional before/after result',
        'fictional_data':True,'no_real_business_claims':True,'output_sha256':sha(output),
        'source_sha256':sha(source),'audio_adts_sha256':audio_hash(output),
        'duration_seconds':float(final['format']['duration']),'resolution':[W,H],
        'fps':FPS,'frames':TOTAL_FRAMES,'audio_sample_rate':48000,
        'technical_av_decode':True,'japanese_caption_visual_review':False,
        'spoken_japanese_independently_verified':False,'semantic_sync_verified':False,
        'asset_rights_verified':False,'reference_v33_compared':False,
        'employee_approved':False,'posting_allowed':False,'auto_post':False,
        'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--genre',default='sales_business',choices=EXAMPLES)
    a=ap.parse_args();print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
