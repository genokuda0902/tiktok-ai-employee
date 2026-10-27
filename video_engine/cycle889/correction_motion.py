"""cycle889: arithmetic-grounded correction motion for 10 genre review shorts.

This is a reimplementation, not the original v33 engine. Render only local,
explicitly hash-pinned, unapproved REVIEW_ONLY MP4; never publish or upload media.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
START=422
END=510
FRAMES=691
TOP=280
BOTTOM=1240
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES=('ai_productivity','beauty','romance_psychology','money_saving','sales_business',
        'career','health_lifestyle','trivia_science','travel_food','product_lifestyle')
TITLES={
 'ai_productivity':'AI集計の数字を照合',
 'beauty':'美容メモの記録を照合',
 'romance_psychology':'会話メモの記録を照合',
 'money_saving':'家計の数字を照合',
 'sales_business':'営業集計の数字を照合',
 'career':'業務記録の数字を照合',
 'health_lifestyle':'生活記録の数字を照合',
 'trivia_science':'検証データを照合',
 'travel_food':'旅程の数字を照合',
 'product_lifestyle':'商品比較の数字を照合'}
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False,'fictional_data':True}

@dataclass(frozen=True)
class Correction:
    genre:str
    label:str
    values:tuple[int,...]
    mistaken_index:int
    mistaken_value:int

    def totals(self):
        if self.genre not in GENRES: raise ValueError('unsupported genre')
        if not self.label or len(self.label)>16 or re.search(r'https?://|@|[\r\n<>]|\d{3}[- ]?\d{4}',self.label):
            raise ValueError('unsafe label')
        if not 2<=len(self.values)<=6 or not all(type(v) is int and 0<=v<=999 for v in self.values):
            raise ValueError('invalid values')
        if not 0<=self.mistaken_index<len(self.values):raise ValueError('invalid index')
        if type(self.mistaken_value) is not int or not 0<=self.mistaken_value<=999:
            raise ValueError('invalid mistaken value')
        if self.mistaken_value==self.values[self.mistaken_index]:raise ValueError('no correction')
        corrected=sum(self.values)
        mistaken=corrected-self.values[self.mistaken_index]+self.mistaken_value
        return mistaken,corrected

EXAMPLE=Correction('ai_productivity','6月 営業A',(12,16,18),2,17)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def validate_manifest(manifest,source):
    if any(manifest.get(k)!=v for k,v in POLICY.items()):raise ValueError('unsafe policy')
    if manifest.get('source_sha256')!=sha256(source):raise ValueError('source hash mismatch')
    return True

def stage(frame):
    if not 0<=frame<END-START:raise ValueError('frame outside scene')
    return 0 if frame<28 else 1 if frame<58 else 2

def safe_geometry():
    return 0<TOP<BOTTOM<1438<1920

def draw_frame(frame,correction=EXAMPLE):
    old,new=correction.totals()
    if not safe_geometry():raise ValueError('unsafe caption geometry')
    st=stage(frame)
    im=Image.new('RGBA',(1080,BOTTOM-TOP),(4,20,39,255))
    d=ImageDraw.Draw(im,'RGBA')
    font=lambda size:ImageFont.truetype(FONT,size,index=0)
    cyan=(82,228,221,255);white=(245,250,255,255);muted=(164,196,217,255);coral=(255,150,140,255)
    d.rounded_rectangle((38,18,1042,965),radius=28,fill=(6,29,51,255),outline=(51,154,178,255),width=3)
    d.rounded_rectangle((66,42,430,104),radius=16,fill=(17,98,125,255))
    d.text((86,49),'BEFORE  →  AFTER',font=font(34),fill=white)
    d.text((65,138),TITLES[correction.genre],font=font(49),fill=white)
    d.text((66,217),'架空データ ｜ 元の値を確認してから修正',font=font(30),fill=muted)
    steps=('① 違いを発見','② 元データを確認','③ 合計を再計算')
    for i,t in enumerate(steps):
        x=63+i*336
        d.rounded_rectangle((x,294,x+310,365),radius=17,
            fill=(13,108,127,255) if i==st else (14,49,69,255),
            outline=cyan if i==st else (45,95,115,255),width=3)
        d.text((x+12,310),t,font=font(28),fill=white)
    d.rounded_rectangle((66,412,1014,578),radius=21,fill=(15,52,77,255))
    d.text((90,433),correction.label,font=font(38),fill=white)
    d.text((90,497),f'{correction.mistaken_value}',font=font(62),fill=coral)
    if st>=1:
        d.line((92,541,157,541),fill=coral,width=6)
        d.text((215,501),'→',font=font(58),fill=muted)
        d.text((340,497),str(correction.values[correction.mistaken_index]),font=font(62),fill=cyan)
        d.text((510,511),'元データと一致',font=font(36),fill=cyan)
    else:
        d.text((210,516),'元データは 18',font=font(37),fill=muted)
    d.rounded_rectangle((66,616,505,815),radius=24,fill=(51,34,52,255),outline=coral,width=3)
    d.rounded_rectangle((543,616,1014,815),radius=24,fill=(12,64,72,255),outline=cyan if st==2 else (60,116,122,255),width=4)
    d.text((93,638),'修正前 合計',font=font(34),fill=white)
    d.text((566,638),'修正後 合計',font=font(34),fill=white)
    d.text((130,690),str(old),font=font(91),fill=coral)
    if st==2:
        d.text((635,690),str(new),font=font(91),fill=cyan)
        d.text((824,733),f'+{new-old}',font=font(38),fill=cyan)
    else:
        d.text((665,716),'検算中…',font=font(38),fill=muted)
    if st==2:
        equation=' + '.join(map(str,correction.values)) + f'  =  {new}'
        d.text((93,857),equation,font=font(44),fill=white)
    else:
        d.text((93,857),('差を見つける' if st==0 else '数字を1つだけ修正'),font=font(43),fill=white)
    d.rounded_rectangle((65,931,1015,945),radius=7,fill=(29,66,85,255))
    progress=int(948*(frame+1)/(END-START))
    d.rounded_rectangle((65,931,65+progress,945),radius=7,fill=cyan)
    return im

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(p)],text=True))

def render(source,output,manifest,work,report):
    source=Path(source);output=Path(output);work=Path(work);report=Path(report)
    validate_manifest(json.loads(Path(manifest).read_text()),source)
    m=probe(source)
    v=next(x for x in m['streams'] if x['codec_type']=='video')
    a=next(x for x in m['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',691):
        raise ValueError('wrong video input')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):raise ValueError('wrong audio input')
    work.mkdir(parents=True,exist_ok=True)
    for f in range(END-START):draw_frame(f).save(work/f'{f:03d}.png',compress_level=1)
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=f"[1:v]setpts=PTS+{START}/({FPS}*TB)[ov];[0:v][ov]overlay=0:{TOP}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(work/'%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v','691','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,timeout=120)
    data={'cycle':889,'source_sha256':sha256(source),'output_sha256':sha256(output),
          'changed_frames':[START,END-1],'changed_seconds':[START/FPS,END/FPS],
          'computed_old_total':EXAMPLE.totals()[0],'computed_new_total':EXAMPLE.totals()[1],
          'full_av_decode':'PASS','audio_elementary':'COPY',
          'japanese_transcript_semantics':'UNVERIFIED','source_rights':'UNVERIFIED',
          'phone_playback':'UNVERIFIED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','output','manifest','work','report'):p.add_argument('--'+name,required=True)
    args=p.parse_args();print(json.dumps(render(args.source,args.output,args.manifest,args.work,args.report),ensure_ascii=False))
