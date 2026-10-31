#!/usr/bin/env python3
"""Private review-only Before/After montage; original screenshot evidence only.

This is a reimplementation, not v33. Output is never approved for posting.
Only frames 609..672 (20.300..22.433s) are changed above y=1460.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W,H,FPS=1080,1920,30
START,END,SAFE_Y=609,673,1460
SOURCE_SHA='0208046ebc210ceb4bfda0ede5005a46cf888510cb7c8326d1f3fb10be5cbbbe'
GENRES=('ai_work','beauty','romance_psychology','money_saving','sales_business','career',
        'health_lifestyle','science_trivia','travel_food','product_comparison_lifestyle')
ACCENTS=dict(zip(GENRES,('#22E1D2','#FA8DB2','#B8A1FA','#FFD16A','#68AEFF',
                         '#81DDA8','#F5B26B','#99D7F9','#F6AD82','#D8B2FF')))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def run(args,binary=False):
    p=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-2500:])
    return p.stdout if binary else p.stdout.decode()


def audio_hash(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()


def validate(path,expected,genre,review_only):
    if not review_only: raise ValueError('review-only required')
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre!='ai_work': raise ValueError('no rights-approved source for genre')
    if expected!=SOURCE_SHA or sha(path)!=SOURCE_SHA: raise ValueError('private source SHA mismatch')
    streams=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',path]))['streams']
    v=[s for s in streams if s['codec_type']=='video']
    a=[s for s in streams if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or v[0]['width']!=W or v[0]['height']!=H or \
       v[0]['r_frame_rate']!='30/1' or int(v[0].get('nb_frames',0))!=691 or \
       a[0]['codec_name']!='aac' or int(a[0]['sample_rate'])!=48000:
        raise ValueError('source video profile mismatch')


def source_still(path,second):
    raw=run(['ffmpeg','-v','error','-ss',str(second),'-i',path,'-frames:v','1',
             '-f','image2pipe','-vcodec','png','-'],True)
    from io import BytesIO
    return Image.open(BytesIO(raw)).convert('RGB')


def crop_evidence(still):
    """Crop only the inherited source's simulated UI, never import new assets."""
    return still.crop((45,390,1035,1200)).resize((388,620),Image.Resampling.LANCZOS)


def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,size)


def frame(n,genre,before,after_prompt,after_check):
    if genre not in ACCENTS: raise ValueError('unknown genre')
    if not 0<=n<END-START: raise ValueError('outside montage')
    accent=ACCENTS[genre]
    img=Image.new('RGB',(W,SAFE_Y),'#061426')
    d=ImageDraw.Draw(img)
    for y in range(0,SAFE_Y,10):
        v=y/SAFE_Y
        d.rectangle((0,y,W,y+9),fill=(int(6+9*v),int(20+13*v),int(38+15*v)))
    d.rounded_rectangle((58,68,1022,220),radius=26,fill='#0D3040',outline='#31546A',width=3)
    d.text((84,88),'BEFORE  /  AFTER',font=font(34,True),fill=accent)
    d.text((84,135),'手作業から「AI＋人の確認」へ',font=font(53,True),fill='white')
    left=(62,285,522,1200);right=(558,285,1018,1200)
    d.rounded_rectangle(left,radius=28,fill='#122538',outline='#7B8A9B',width=3)
    d.rounded_rectangle(right,radius=28,fill='#0A303A',outline=accent,width=4)
    d.rounded_rectangle((86,306,500,390),radius=18,fill='#3C4350')
    d.text((107,321),'BEFORE  手作業',font=font(36,True),fill='white')
    d.rounded_rectangle((580,306,997,390),radius=18,fill='#155E60')
    d.text((602,321),'AFTER  AI＋検算',font=font(36,True),fill='white')
    # Evidence comes only from the source MP4. This is a montage, not live operation.
    img.paste(ImageEnhance.Color(before).enhance(0.38),(98,416))
    # Introduce the after card with a short horizontal reveal, then show checking evidence.
    reveal=max(0,min(1,(n-9)/15))
    if reveal:
        evidence=after_prompt if n<40 else after_check
        w=int(388*reveal)
        img.paste(evidence.crop((0,0,w,620)),(594,416))
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((100,1063,484,1168),radius=14,fill='#243A4B')
    d.text((115,1077),'毎回、最初から作業',font=font(29,True),fill='#E9F1F5')
    if n>=24:
        d.rounded_rectangle((594,1063,983,1168),radius=14,fill='#0B6565')
        d.text((605,1077),'下書き → 自分で検算',font=font(27,True),fill='white')
    d.rounded_rectangle((62,1230,1018,1374),radius=24,fill='#0C2C3D',outline='#335A6C',width=2)
    d.text((90,1250),'操作イメージ / 架空データ / 効果時間は未計測',font=font(29),fill='#C3DDE4')
    d.rectangle((90,1335,90+int(900*(n+1)/(END-START)),1343),fill=accent)
    return img


def render(source,output,expected,genre='ai_work',review_only=False):
    validate(source,expected,genre,review_only)
    a=audio_hash(source)
    before=crop_evidence(source_still(source,4.1))
    prompt=crop_evidence(source_still(source,9.8))
    check=crop_evidence(source_still(source,12.5))
    with tempfile.TemporaryDirectory(prefix='cycle1048_') as temp:
        folder=Path(temp)
        for n in range(END-START):
            frame(n,genre,before,prompt,check).save(folder/f'{n:03d}.png',optimize=True)
        filt=f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',str(FPS),'-i',str(folder/'%03d.png'),'-filter_complex',filt,
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',output])
    if audio_hash(output)!=a: raise RuntimeError('AAC payload changed')
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    return {'source_sha256':sha(source),'output_sha256':sha(output),'audio_adts_sha256':a,
            'changed_frames':[START,END-1],'protected_caption_y':SAFE_Y,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--source-sha',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--review-only',action='store_true');p.add_argument('--report')
    x=p.parse_args()
    result=render(x.source,x.output,x.source_sha,x.genre,x.review_only)
    if x.report: Path(x.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))
