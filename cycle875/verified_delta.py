"""cycle875: source-verified before/after scene for ten genres, PRIVATE REVIEW ONLY.

Reimplementation, not v33 source. Never publish inherited media without approval.
Scene 06 only: the earlier 17 -> 18 animation lacked clear source evidence.
Now the 3-step sequence makes the source value and recalculation explicit.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from cycle874.chart_truth import GENRES, validate_genre

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, COUNT, TOP, BOTTOM = 422, 88, 285, 1450
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

@lru_cache(maxsize=64)
def font(n,bold=True):return ImageFont.truetype(FONT if bold else REGULAR,n)

def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)

def evidence(genre):
 g=validate_genre(genre)
 before=g.a[2]-1
 if before<=0:raise ValueError('before must be positive')
 return {'period':g.period[2],'label':g.label_a,'before':before,'after':g.a[2],
         'source_a':g.a,'source_b':g.b,'total_a':sum(g.a),'total_b':sum(g.b)}

@lru_cache(maxsize=1)
def background():
 im=Image.new('RGB',(WIDTH,BOTTOM-TOP));d=ImageDraw.Draw(im)
 for y in range(BOTTOM-TOP):
  k=y/(BOTTOM-TOP)
  d.line((0,y,WIDTH,y),fill=(8+int(5*k),23+int(20*k),43+int(31*k)))
 return im

def safe_text(d,xy,s,maxwidth,sz,fill,bold=True):
 f=font(sz,bold)
 if d.textbbox((0,0),s,font=f)[2]-d.textbbox((0,0),s,font=f)[0]>maxwidth:
  raise ValueError('text exceeds safe layout: '+s)
 d.text(xy,s,font=f,fill=fill)

def frame(i,genre='ai_work'):
 if not 0<=i<COUNT:raise ValueError('invalid scene frame')
 e=evidence(genre);im=background().copy();d=ImageDraw.Draw(im,'RGBA')
 cyan=(68,221,234); white=(244,250,255); muted=(174,204,223)
 d.rounded_rectangle((56,25,370,84),radius=23,fill=(13,77,96,255),outline=cyan,width=2)
 safe_text(d,(82,35),'BEFORE  →  AFTER',285,29,white)
 safe_text(d,(54,114),'1箇所の違いを見つける',925,53,white)
 safe_text(d,(58,188),'架空データの修正例  /  元データと照合',965,34,muted,False)
 # Two large source-driven cards, no fabricated performance claim.
 for x,title,col in ((56,'修正前',(255,170,157)),(554,'元データ＝修正後',(85,233,218))):
  d.rounded_rectangle((x,275,x+470,592),radius=27,fill=(17,39,61,255),outline=col,width=4)
  safe_text(d,(x+29,299),title,380,37,white)
  safe_text(d,(x+105,376),str(e['before'] if x==56 else e['after']),270,115,col)
  safe_text(d,(x+32,520),f"{e['period']}  {e['label']}",385,35,muted)
 # Visual pulse draws attention to the corrected value, not to unsupported statistics.
 t=ease((i-18)/27)
 if t>0:
  d.rounded_rectangle((392,406,684,470),radius=30,fill=(18,102,125,int(210*t)),outline=cyan,width=3)
  safe_text(d,(433,414),'照合  →',235,33,white)
 # Always expose complete original data and mathematically derived totals.
 d.rounded_rectangle((55,629,1025,919),radius=23,fill=(9,39,56,255),outline=(62,145,173),width=3)
 safe_text(d,(84,646),'元データで再計算',810,40,white)
 a=e['source_a'];b=e['source_b'];p=GENRES[genre].period
 for j in range(3):
  x=92+j*302
  d.rounded_rectangle((x,721,x+266,793),radius=12,fill=(24,75,94,255))
  safe_text(d,(x+14,732),f'{p[j]}  {a[j]} / {b[j]}',238,32,white)
 if i>=48:
  # Source-derived, not arbitrary totals. Both series use the same inputs as cycle874.
  safe_text(d,(89,831),f"{e['label']}  {a[0]}+{a[1]}+{a[2]}={e['total_a']}",880,38,cyan)
  if genre=='ai_work':
   safe_text(d,(626,831),f"営業B  {e['total_b']}",366,34,white)
 d.rounded_rectangle((56,976,1025,1102),radius=23,fill=(15,65,83,255),outline=(51,162,181),width=2)
 safe_text(d,(94,1008),'違いを見つけたら、1箇所ずつ修正',925,42,white)
 # A tiny dynamic step cue; all labels remain within scene safe zone.
 step='01  発見' if i<28 else ('02  修正' if i<55 else '03  検算')
 d.rounded_rectangle((716,31,1025,87),radius=22,fill=(14,63,87,255),outline=(55,164,189),width=2)
 safe_text(d,(760,39),step,235,31,white)
 return im

def render(source,output,manifest,genre='ai_work',start=START,count=COUNT,total=FRAMES):
 source,output=Path(source),Path(output)
 if output.exists():raise ValueError('refuse overwrite')
 if not source.is_file():raise FileNotFoundError('source missing')
 if manifest!={**POLICY,'source_sha256':sha(source)}:raise ValueError('private manifest rejected')
 evidence(genre)
 if count<1 or count>COUNT or start<0 or start+count>total:raise ValueError('invalid frame range')
 with tempfile.TemporaryDirectory(prefix='cycle875_') as td:
  for i in range(count):frame(i,genre).save(Path(td)/f'{i:03}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{start}/({FPS}*TB)[overlay];'
        f'[0:v][overlay]overlay=x=0:y={TOP}:enable=\'between(n,{start},{start+count-1})\':'
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
       '-framerate',str(FPS),'-i',str(Path(td)/'%03d.png'),'-filter_complex',filt,
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20',
       '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(total),'-c:a','copy',
       '-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=300)
 return {'source_sha256':sha(source),'output_sha256':sha(output),'scene':6,
         'start_frame':start,'changed_frames':count,'genres':len(GENRES),
         'evidence':evidence(genre),'policy':POLICY}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('source','output','manifest','report'):p.add_argument('--'+k,required=True)
 p.add_argument('--genre',default='ai_work');a=p.parse_args()
 r=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))