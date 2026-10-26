"""cycle877: truthful full-height bar reveal; review-only ten-genre reimplementation.

Avoid the intermediate false rank from growing each bar from zero at different times.
Only fully scaled bars become visible, one complete month/group at a time.
Original private MP4, inherited narration and caption strip are never committed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from cycle874.chart_truth import GENRES, validate_genre

W,H,FPS,FRAMES=1080,1920,30,691
START,COUNT,TOP,BOTTOM=170,81,285,1245
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}
REVEAL_FRAMES=(9,26,43)

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

@lru_cache(maxsize=40)
def font(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)

def bar_heights(g):
 peak=max(*g.a,*g.b)
 return tuple(round(270*v/peak) for v in g.a),tuple(round(270*v/peak) for v in g.b)

def revealed_groups(i):
 if not 0<=i<COUNT:raise ValueError('out-of-range frame')
 return tuple(j for j,threshold in enumerate(REVEAL_FRAMES) if i>=threshold)

def bar_state(i,genre):
 g=validate_genre(genre)
 a,b=bar_heights(g)
 return tuple({'period':g.period[j], 'a':g.a[j],'b':g.b[j],
               'a_height':a[j],'b_height':b[j]} for j in revealed_groups(i))

def text(d,xy,s,size=34,fill='#F5FCFF',bold=True,maxw=None):
 f=font(size,bold)
 if maxw is not None and d.textbbox((0,0),s,font=f)[2]>maxw:
  raise ValueError('clipped text: '+s)
 d.text(xy,s,font=f,fill=fill)

def render_frame(i,genre='ai_work'):
 g=validate_genre(genre)
 state=bar_state(i,genre)
 im=Image.new('RGB',(W,BOTTOM-TOP));d=ImageDraw.Draw(im)
 for y in range(BOTTOM-TOP):
  k=y/(BOTTOM-TOP)
  d.line((0,y,W,y),fill=(9+round(5*k),25+round(15*k),43+round(14*k)))
 d.rounded_rectangle((50,27,514,92),radius=20,fill='#164F63',outline='#64CFE0',width=2)
 text(d,(74,44),'DATA / 架空データ・確認用',29,maxw=420)
 text(d,(52,118),g.headline,50,maxw=970)
 text(d,(53,197),'数値を先に提示 → 確定した棒だけ表示',32,fill='#A4DDE8',bold=False,maxw=973)
 d.rounded_rectangle((52,270,1028,414),radius=22,fill='#102D44',outline='#317E96',width=3)
 text(d,(81,281),'元データ',32)
 for j,(period,va,vb) in enumerate(zip(g.period,g.a,g.b)):
  x=84+316*j
  d.rounded_rectangle((x,330,x+294,392),radius=14,fill='#1A5061')
  text(d,(x+12,344),f'{period}  {va} / {vb}',29,maxw=273)
 d.rounded_rectangle((52,437,1028,866),radius=24,fill='#0D2439',outline='#327A92',width=3)
 text(d,(78,458),'元データ → 完成した棒グラフ',33)
 d.ellipse((635,467,653,485),fill='#4FD5E3')
 text(d,(663,458),g.label_a,27,maxw=140)
 d.ellipse((837,467,855,485),fill='#F7B668')
 text(d,(866,458),g.label_b,27,maxw=140)
 base=796
 d.line((98,base,977,base),fill='#7999AB',width=3)
 for j,(period,va,vb) in enumerate(zip(g.period,g.a,g.b)):
  cx=225+308*j
  if j in revealed_groups(i):
   ah,bh=bar_heights(g)
   d.rounded_rectangle((cx-63,base-ah[j],cx+3,base),radius=9,fill='#43CFDF')
   d.rounded_rectangle((cx+20,base-bh[j],cx+86,base),radius=9,fill='#F7B668')
   text(d,(cx-57,base-ah[j]-41),str(va),28)
   text(d,(cx+27,base-bh[j]-41),str(vb),28)
  else:
   d.rounded_rectangle((cx-71,base-55,cx+94,base-10),radius=12,fill='#193C4B')
   text(d,(cx-30,base-52),'準備中',23,fill='#A6C6D1',maxw=125)
  text(d,(cx-30,806),period,31,maxw=90)
 if i>=60:
  d.rounded_rectangle((54,886,1026,941),radius=14,fill='#14576A')
  msg=f'検算OK：{g.label_a} {sum(g.a)}  ／  {g.label_b} {sum(g.b)}'
  text(d,(80,891),msg,32,maxw=923)
 else:
  text(d,(59,899),'全グループ表示後に合計を照合',28,fill='#9EC6D6',bold=False,maxw=963)
 return im

def render(source,output,manifest,genre='ai_work'):
 source,output=Path(source),Path(output)
 if output.exists():raise ValueError('refuse overwrite')
 if not source.is_file():raise FileNotFoundError(source)
 if manifest!={**POLICY,'source_sha256':sha(source)}:raise ValueError('fail closed: invalid review manifest')
 validate_genre(genre)
 with tempfile.TemporaryDirectory(prefix='cycle877_') as td:
  for i in range(COUNT):render_frame(i,genre).save(Path(td)/f'{i:03d}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/({FPS}*TB)[ov];'
        f'[0:v][ov]overlay=0:{TOP}:enable=\'between(n,{START},{START+COUNT-1})\':'
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
       '-framerate',str(FPS),'-i',str(Path(td)/'%03d.png'),'-filter_complex',filt,
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20',
       '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(FRAMES),'-c:a','copy',
       '-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=300)
 return {'source_sha256':sha(source),'output_sha256':sha(output),'changed_frames':COUNT,
         'start_frame':START,'ten_genres_supported':len(GENRES),'policy':POLICY,
         'reveal_frames':REVEAL_FRAMES,'data':{'periods':g.period if (g:=GENRES[genre]) else (),
                                             'a':g.a,'b':g.b}}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for x in ('source','output','manifest','report'):p.add_argument('--'+x,required=True)
 p.add_argument('--genre',default='ai_work');a=p.parse_args()
 r=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False))
