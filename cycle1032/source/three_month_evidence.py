#!/usr/bin/env python3
"""Cycle1032 review-only three-month evidence chart repair.

This is a REIMPLEMENTATION, not original v33 source. Does not publish or upload
private media. Replaces only a demonstrably incomplete 4-6月 chart with a
verified arithmetic example; preserves inherited audio and burned subtitles.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

GENRES = frozenset((
    'ai_work','beauty','romance_psychology','money_saving','sales_business',
    'career','health_lifestyle','science_trivia','travel_food',
    'product_comparison_lifestyle',
))
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W,H,FPS=1080,1920,30
SAFE_SUBTITLE_Y=1490
BEATS=((342,370),(371,399),(400,428))  # 11.40–14.30s, source 30fps
SYNTH_BEATS=((6,21),(22,37),(38,53)) # 0.2–1.8s, 2s CI fixture

@dataclass(frozen=True)
class Evidence:
    genre: str
    categories: tuple[str,str,str]
    series_a: tuple[int,int,int]
    series_b: tuple[int,int,int]
    label_a: str
    label_b: str
    fictional: bool
    provenance: str

    def validate(self):
        if self.genre not in GENRES: raise ValueError('unknown genre')
        if not self.fictional or self.provenance!='fictional_educational_example':
            raise ValueError('non-approved data provenance; fail closed')
        if len(self.categories)!=3 or any(not c or len(c)>8 for c in self.categories):
            raise ValueError('three concise category labels required')
        if not self.label_a or not self.label_b or len(self.label_a)>12 or len(self.label_b)>12:
            raise ValueError('invalid series labels')
        for vals in (self.series_a,self.series_b):
            if len(vals)!=3 or any(type(x) is not int or x<0 or x>30 for x in vals):
                raise ValueError('three bounded nonnegative integer samples required')
        if max(*self.series_a,*self.series_b)==0: raise ValueError('empty example')

DEFAULT_EXAMPLE=Evidence('ai_work',('4月','5月','6月'),(12,16,18),(8,9,12),
                         '営業A','営業B',True,'fictional_educational_example')

def run(args,binary=False):
    p=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('command failed: '+ ' '.join(str(x) for x in args[:6])+'\n'+p.stderr.decode(errors='replace')[-2500:])
    return p.stdout if binary else p.stdout.decode()

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()

def font(sz,bold=False):
    p=FONT_BOLD if bold else FONT_REG
    if not Path(p).is_file(): raise RuntimeError('Noto CJK fonts required')
    return ImageFont.truetype(p,sz)

def draw_panel(data:Evidence,active:int)->Image.Image:
    """Full-frame transparent RGBA with 3-month chart strictly above subtitle zone."""
    data.validate()
    if active not in (0,1,2):raise ValueError('active beat must be 0,1,2')
    s=2
    im=Image.new('RGBA',(W*s,H*s),(0,0,0,0));d=ImageDraw.Draw(im)
    def box(xy,fill,r=0,outline=None,width=1):
        d.rounded_rectangle(tuple(round(v*s) for v in xy),radius=r*s,fill=fill,outline=outline,width=width*s)
    def text(xy,words,sz,color,bold=False,anchor=None):
        d.text((xy[0]*s,xy[1]*s),words,font=font(sz*s,bold),fill=color,anchor=anchor)
    box((62,304,1018,1278),(5,34,49,255),28,outline=(44,185,196,255),width=3)
    box((86,326,994,411),(7,57,72,255),15)
    text((111,340),'4〜6月の数値を検算',45,'#ffffff',True)
    box((797,342,970,391),(15,79,88,255),13,outline=(67,207,196,255),width=2)
    text((817,348),'架空の例',28,'#bafaf0',True)
    text((106,426),'営業Aと営業Bを月別に比較',29,'#c4dfe4')
    box((608,430,637,459),(23,218,202,255),6);text((647,426),data.label_a,27,'#e7ffff')
    box((798,430,827,459),(143,155,242,255),6);text((837,426),data.label_b,27,'#e7ffff')
    # Draw a complete, honest chart: all 6 bars visible in all 3 beats.
    left,right,top,bottom=145,953,503,933
    max_y=20 if max(*data.series_a,*data.series_b)<=20 else 30
    for val in range(0,max_y+1,5):
        y=bottom-(val/max_y)*(bottom-top)
        d.line((left*s,y*s,right*s,y*s),fill=(71,117,130,125),width=2*s)
        text((112,int(y)-18),str(val),23,'#b7d0d8')
    centers=(287,554,821)
    for i,(category,a,b) in enumerate(zip(data.categories,data.series_a,data.series_b)):
        cx=centers[i]
        if i==active:box((cx-116,482,cx+118,1010),(12,81,91,255),16,outline=(66,229,213,255),width=3)
        for j,(val,col) in enumerate(((a,(23,218,202,255)),(b,(143,155,242,255)))):
            x=cx-79+j*87; bh=(val/max_y)*(bottom-top)
            box((x,bottom-bh,x+69,bottom),col,10)
            text((x+34,bottom-bh-43),str(val),31,'#ffffff',True,anchor='mt')
        text((cx,956),category,32,'#ffffff',True,anchor='mt')
    # Separate totals with arithmetic check to avoid the old missing-June error.
    box((91,1030,988,1160),(11,63,76,255),17,outline=(60,162,175,255),width=2)
    text((116,1042),'3か月合計',32,'#b8dfe6',True)
    text((342,1035),f'{data.label_a} {sum(data.series_a)}',45,'#31e8d5',True)
    text((683,1035),f'{data.label_b} {sum(data.series_b)}',45,'#acb9ff',True)
    text((120,1101),f'{"+".join(map(str,data.series_a))}={sum(data.series_a)}',27,'#d8faf7')
    text((700,1101),f'{"+".join(map(str,data.series_b))}={sum(data.series_b)}',27,'#e5e7ff')
    text((108,1202),'※ 説明用の架空データ。実績ではありません。',26,'#c6dbe1')
    # Guaranteed transparent pixels in subtitle area.
    return im.resize((W,H),Image.Resampling.LANCZOS)

def graph(beats):
    if len(beats)!=3 or any(a<0 or b<a for a,b in beats):raise ValueError('invalid beats')
    if any(beats[i][1]+1!=beats[i+1][0] for i in (0,1)):raise ValueError('gapped beats')
    filters=[];src='0:v'
    for i,(a,b) in enumerate(beats):
        dest=f'v{i}'
        filters.append(f"[{src}][{i+1}:v]overlay=x=0:y=0:enable='between(n,{a},{b})':eof_action=pass[{dest}]")
        src=dest
    return ';'.join(filters)

def render(source,output,report,expected_sha,genre='ai_work',review_only=False,synthetic_ci=False):
    if not review_only:raise ValueError('human review gate required')
    if genre!='ai_work':raise ValueError('full video requires matching approved genre-specific source')
    source,output,report=map(lambda x:Path(x).resolve(),(source,output,report))
    if not source.is_file() or source==output or output.exists() or report.exists():
        raise ValueError('source missing or output/report already exists')
    if len(expected_sha)!=64 or sha256(source)!=expected_sha:raise ValueError('source SHA mismatch')
    p=probe(source)
    v=[s for s in p['streams'] if s['codec_type']=='video'];a=[s for s in p['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or len(p['streams'])!=2:raise ValueError('exactly one A/V stream required')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],a[0]['codec_name'],int(a[0]['sample_rate']))!=('h264',1080,1920,'30/1','aac',48000):
        raise ValueError('unexpected source format')
    beats=SYNTH_BEATS if synthetic_ci else BEATS
    if int(v[0].get('nb_frames',0))<beats[-1][1]+1:raise ValueError('not enough frames')
    output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        pngs=[]
        for i in range(3):
            f=Path(td)/f'beat{i}.png';draw_panel(DEFAULT_EXAMPLE,i).save(f);pngs.append(f)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',source]
        for f in pngs:cmd+=['-loop','1','-framerate','30','-i',f]
        cmd+=['-filter_complex',graph(beats),'-map','[v2]','-map','0:a:0','-c:v','libx264',
              '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2',
              '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart','-t',str(float(p['format']['duration'])),'-frames:v',str(int(v[0]['nb_frames'])),output]
        run(cmd)
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    q=probe(output);vv=next(s for s in q['streams'] if s['codec_type']=='video')
    if (vv['width'],vv['height'],vv['r_frame_rate'],int(vv.get('nb_frames',0)))!=(1080,1920,'30/1',int(v[0]['nb_frames'])):
        raise RuntimeError('video metadata mismatch')
    if audio_sha(source)!=audio_sha(output):raise RuntimeError('audio bitstream changed')
    result={'source_sha256':sha256(source),'output_sha256':sha256(output),'genre':genre,
      'duration_seconds':float(q['format']['duration']),'frames':int(vv['nb_frames']),
      'video':'H.264 1080x1920 30fps','audio':'AAC 48kHz jpn-tagged',
      'audio_bitstream_unchanged':True,'full_av_decode':'PASS','fictional_example':True,
      'chart_months':list(DEFAULT_EXAMPLE.categories),'series_a':list(DEFAULT_EXAMPLE.series_a),
      'series_b':list(DEFAULT_EXAMPLE.series_b),'total_a':sum(DEFAULT_EXAMPLE.series_a),
      'total_b':sum(DEFAULT_EXAMPLE.series_b),'change':'replace missing June bars with complete 3-month chart and verified totals; 3 guided beats',
      'change_frames':list(map(list,beats)),'protected_subtitle_y_min':SAFE_SUBTITLE_Y,
      'independent_japanese_asr':'NOT_PERFORMED','caption_semantic_sync':'NOT_VERIFIED',
      'source_rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','output','report','expected-source-sha'):ap.add_argument('--'+k,required=True)
    ap.add_argument('--genre',choices=sorted(GENRES),default='ai_work')
    ap.add_argument('--review-only',action='store_true');ap.add_argument('--synthetic-ci',action='store_true')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.report,args.expected_source_sha,args.genre,args.review_only,args.synthetic_ci),ensure_ascii=False))
