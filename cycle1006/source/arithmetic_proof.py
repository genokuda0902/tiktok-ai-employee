#!/usr/bin/env python3
"""Private review-only arithmetic provenance card for an image-first short.

This is a new reimplementation, NOT original v33. It never uploads source media.
Other genres fail closed until independent scene/rights review. No posting path.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
APPROVED_FOR_PRIVATE_TEST = ('ai_work',)
A = (12,16,18)
B = (8,9,12)
TOTALS = (46,29)
WINDOW = (12.95,14.45)
BOX = (75,972,930,194) # x,y,width,height; protected captions begin y=1280
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def verify_ledger(a=A,b=B,totals=TOTALS,fictional=True):
    if not fictional: raise ValueError('source provenance missing: only explicitly fictional demo data allowed')
    if not all(isinstance(v,int) and not isinstance(v,bool) and 0<=v<=999 for v in (*a,*b)):
        raise ValueError('ledger must contain safe nonnegative integer example data')
    if len(a)!=3 or len(b)!=3 or (sum(a),sum(b))!=tuple(totals):
        raise ValueError('source numbers and displayed totals disagree')
    return True

def check_policy(genre,review_only,source_sha):
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre not in APPROVED_FOR_PRIVATE_TEST: raise ValueError('genre has not passed private review')
    if not review_only: raise ValueError('HUMAN_REVIEW only; release is forbidden')
    if len(source_sha)!=64 or any(c not in '0123456789abcdef' for c in source_sha.lower()):
        raise ValueError('pinned source sha256 required')

def font(sz):
    return ImageFont.truetype(FONT,sz)

def create_card(path,a=A,b=B,totals=TOTALS):
    verify_ledger(a,b,totals)
    w,h=BOX[2:]
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,w-2,h-2),radius=25,fill=(3,31,49,248),outline=(74,209,223,255),width=3)
    d.rounded_rectangle((15,12,w-15,51),radius=10,fill=(14,67,83,255))
    d.text((30,17),'元データから合計を検算',font=font(25),fill=(230,250,255,255))
    d.text((640,21),'説明用の架空データ',font=font(16),fill=(173,219,225,255))
    d.line((w//2,66,w//2,h-14),fill=(50,121,141,255),width=2)
    for x,label,nums,total,color in ((30,'営業A',a,totals[0],(52,235,212,255)),(w//2+24,'営業B',b,totals[1],(153,172,255,255))):
        d.text((x,67),label,font=font(24),fill=color)
        formula=' + '.join(str(v) for v in nums)
        d.text((x,103),formula,font=font(31),fill=(245,251,255,255))
        d.text((x+220,102),f'= {total}',font=font(34),fill=color)
        d.text((x,153),'4月   5月   6月',font=font(17),fill=(151,199,210,255))
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
    return path

def probe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],check=True,capture_output=True,text=True)
    return json.loads(p.stdout)

def check_media(meta):
    s=meta['streams'];v=next((x for x in s if x['codec_type']=='video'),None)
    a=next((x for x in s if x['codec_type']=='audio'),None)
    sub=next((x for x in s if x['codec_type']=='subtitle'),None)
    if not v or (v.get('width'),v.get('height'),v.get('r_frame_rate'))!=(1080,1920,'30/1'):
        raise ValueError('expected 1080x1920 30fps video')
    if not a or a.get('sample_rate')!='48000' or a.get('codec_name')!='aac':
        raise ValueError('expected AAC 48kHz narration track')
    if not sub or sub.get('codec_name')!='mov_text':raise ValueError('selectable Japanese subtitle track required')
    if a.get('tags',{}).get('language')!='jpn' or sub.get('tags',{}).get('language')!='jpn':
        raise ValueError('Japanese stream metadata required')

def build_command(source,card,output,window=WINDOW):
    start,end=window
    if not (0<=start<end and end-start>=0.8):raise ValueError('unsafe time window')
    dur=end-start
    fade=min(0.18,dur/6)
    vf=(f'[1:v]format=rgba,fade=t=in:st=0:d={fade}:alpha=1,'
        f'fade=t=out:st={dur-fade}:d={fade}:alpha=1,'
        f'setpts=PTS-STARTPTS+{start}/TB[proof];'
        f'[0:v][proof]overlay=x={BOX[0]}:y={BOX[1]}:eof_action=pass:shortest=0:'
        f"enable='between(t,{start},{end})'[v]")
    return ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
            '-loop','1','-framerate','30','-t',str(dur),'-i',str(card),
            '-filter_complex',vf,'-map','[v]','-map','0:a:0','-map','0:s:0',
            '-c:v','libx264','-preset','ultrafast','-crf','18','-pix_fmt','yuv420p',
            '-c:a','copy','-c:s','copy','-metadata:s:a:0','language=jpn',
            '-metadata:s:s:0','language=jpn','-movflags','+faststart',str(output)]

def render(source,output,card,report,expected_sha,genre='ai_work',review_only=False,window=WINDOW):
    check_policy(genre,review_only,expected_sha)
    verify_ledger()
    source,output,report=map(Path,(source,output,report))
    if not source.is_file() or source.resolve()==output.resolve():raise ValueError('invalid source')
    actual=sha256(source)
    if actual!=expected_sha:raise ValueError('source SHA mismatch')
    check_media(probe(source))
    create_card(card)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=build_command(source,card,output,window)
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-1800:])
    result={'genre':genre,'review_only':True,'publication_approved':False,'source_sha256':actual,
            'output_sha256':sha256(output),'window_seconds':list(window),'ledger':{'A':list(A),'B':list(B),'totals':list(TOTALS),'fictional':True},
            'card_roi':BOX,'caption_safe_start_y':1280,'narration_transcribed':'NOT_VERIFIED','smartphone_playback':'NOT_VERIFIED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','card','report','expected-sha'):p.add_argument('--'+n,required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--review-only',action='store_true')
    x=p.parse_args()
    print(json.dumps(render(x.source,x.output,x.card,x.report,x.expected_sha,x.genre,x.review_only),ensure_ascii=False))
