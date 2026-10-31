#!/usr/bin/env python3
"""Review-only, source-reused three-shot recap. Never uploads or posts media."""
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30; WIDTH=1080; HEIGHT=1920; START=609; END=691
SAFE_TOP=1280
SHOTS=((195,'01','完成見本を用意'),(303,'02','目的と条件を入力'),(474,'03','数字を自分で検算'))
GENRES=('ai_work','beauty','romance_psychology','money_saving','sales_business','career','health_lifestyle','science_trivia','travel_food','product_comparison_lifestyle')
COLORS={'ai_work':'#42E9D0','beauty':'#FFB7D5','romance_psychology':'#C4A9FF','money_saving':'#F6CD69','sales_business':'#5EB8F4','career':'#89C7FF','health_lifestyle':'#7CE4B0','science_trivia':'#9CDEEF','travel_food':'#F3C777','product_comparison_lifestyle':'#FFAD79'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def run(args,binary=False):
    p=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout if binary else p.stdout.decode()

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def audio_sha(path):return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()

def source_frame(path,number):
    data=run(['ffmpeg','-v','error','-ss',str(number/FPS),'-i',path,'-frames:v','1','-f','image2pipe','-vcodec','png','-'],True)
    from io import BytesIO
    return Image.open(BytesIO(data)).convert('RGB')

def stage_for_frame(n):
    if n<START or n>=END:raise ValueError('frame outside recap')
    offset=n-START
    return min(offset//21,3)

def layout(n,stills,genre='ai_work'):
    if genre not in GENRES:raise ValueError('unknown genre')
    if len(stills)!=3:raise ValueError('requires three verified source frames')
    stage=stage_for_frame(n); accent=COLORS[genre]
    im=Image.new('RGBA',(WIDTH,SAFE_TOP),(5,15,31,255));d=ImageDraw.Draw(im)
    title=ImageFont.truetype(FONT,58);body=ImageFont.truetype(FONT,44);small=ImageFont.truetype(FONT,31)
    d.text((70,82),'3カットで復習',font=title,fill='white')
    d.rounded_rectangle((70,176,1010,191),radius=7,fill=(29,65,79,255))
    d.rounded_rectangle((70,176,70+int(940*(n-START+1)/(END-START)),191),radius=7,fill=accent)
    if stage<3:
        f=stills[stage].copy()
        f=f.crop((90,140,990,1120)).resize((760,827),Image.Resampling.LANCZOS)
        im.paste(f,(160,265))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((100,218,980,338),radius=24,fill=(5,24,41,245),outline=accent,width=5)
        d.text((138,236),f'{SHOTS[stage][1]}  {SHOTS[stage][2]}',font=body,fill='white')
        d.rounded_rectangle((100,1100,980,1196),radius=20,fill=(4,29,47,255),outline=accent,width=3)
        d.text((155,1116),'実際の操作イメージ / 再掲',font=small,fill=accent)
    else:
        d.rounded_rectangle((95,360,985,920),radius=45,fill=(8,38,54,255),outline=accent,width=7)
        d.text((185,480),'今日から1つだけ',font=title,fill='white')
        d.text((190,650),'作業を選んで試そう',font=body,fill=accent)
        d.text((220,785),'保存して、明日も使う',font=small,fill='white')
    for j in range(3):
        x=425+j*80
        d.ellipse((x,1222,x+25,1247),fill=accent if j==min(stage,2) else '#36515F')
    return im

def validate(source,expected_sha,genre):
    if genre!='ai_work':raise ValueError('unapproved genre source: fail closed')
    if sha(source)!=expected_sha:raise ValueError('source SHA mismatch')
    p=probe(source);v=[s for s in p['streams'] if s['codec_type']=='video'];a=[s for s in p['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or len(p['streams'])!=2:raise ValueError('requires one video and audio')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(v[0]['nb_frames']),a[0]['codec_name'],int(a[0]['sample_rate']))!=('h264',1080,1920,'30/1',691,'aac',48000):raise ValueError('source format')

def render(source,dest,report,expected_sha,genre='ai_work',review_only=False):
    source,dest,report=map(Path,(source,dest,report))
    if not review_only:raise ValueError('human review required')
    if dest.exists() or report.exists() or len({source.resolve(),dest.resolve(),report.resolve()})!=3:raise ValueError('destination exists or collides')
    validate(source,expected_sha,genre)
    stills=[source_frame(source,s[0]) for s in SHOTS]
    dest.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='recap1038_') as t:
        t=Path(t)
        for n in range(START,END):layout(n,stills,genre).save(t/f'{n-START:03d}.png')
        run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',source,
             '-itsoffset',str(START/FPS),'-framerate',str(FPS),'-i',t/'%03d.png',
             '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]',
             '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p',
             '-frames:v','691','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',dest])
    run(['ffmpeg','-v','error','-xerror','-i',dest,'-f','null','-'])
    p=probe(dest);v=next(s for s in p['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],int(v['nb_frames']))!=(1080,1920,691):raise RuntimeError('bad output video')
    if audio_sha(source)!=audio_sha(dest):raise RuntimeError('audio changed')
    result={'source_sha256':expected_sha,'output_sha256':sha(dest),'frames':691,'duration':float(p['format']['duration']),
      'recap_start_frame':START,'three_evidence_source_frames':[s[0] for s in SHOTS],
      'three_recap_shots_plus_cta':True,'subtitle_region_y_min':SAFE_TOP,'audio_adts_sha256':audio_sha(dest),
      'full_decode':'PASS','japanese_speech_semantics':'NOT_VERIFIED','rights':'NOT_VERIFIED','approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ('source','dest','report','expected-sha'):p.add_argument('--'+x,required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--review-only',action='store_true')
    a=p.parse_args();print(json.dumps(render(a.source,a.dest,a.report,a.expected_sha,a.genre,a.review_only),ensure_ascii=False))
