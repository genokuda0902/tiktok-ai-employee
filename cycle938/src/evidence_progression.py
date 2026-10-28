#!/usr/bin/env python3
"""cycle938: three-beat fictional evidence comparison, review-only.

All private source media remain local. No actual Excel/ChatGPT recording is
claimed; numbers 17 and 18 are fictional values from the inherited scene06.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS,NFRAMES=1080,1920,30,691
START,END=435,522
SAFE_Y=1445
POLICY='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={'ai_work':'AI仕事術','finance':'家計・金融','health':'健康','travel':'旅行','beauty':'美容','cooking':'料理','education':'学習','career':'仕事・転職','lifestyle':'暮らし','technology':'テクノロジー'}
def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
 return h.hexdigest()
def check(genre,expected_sha=None):
 if genre not in GENRES or len(GENRES)!=10:raise ValueError('unsupported genre')
 if END-START!=87 or SAFE_Y>1450 or not POLICY.endswith('PUBLICATION_NOT_APPROVED'):raise RuntimeError('timing/safety guard failed')
 if not Path(FONT).exists() or not Path(BOLD).exists():raise FileNotFoundError('Japanese fonts unavailable')
 if expected_sha is not None and len(expected_sha)!=64:raise ValueError('full source SHA256 required')
def phase(frame):
 if not 0<=frame<END-START:raise ValueError('frame outside scene06')
 return frame//29
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def card(d,xy,fill,outline,width=3,radius=25):
 d.rounded_rectangle(xy,radius=radius,fill=fill,outline=outline,width=width)
def render_frame(local,genre='ai_work',draft='17',source='18'):
 check(genre)
 if not(draft.isdigit() and source.isdigit() and len(draft)<=3 and len(source)<=3):raise ValueError('explicit short numeric values required')
 p=phase(local)
 img=Image.new('RGB',(W,SAFE_Y),(5,20,35));d=ImageDraw.Draw(img)
 for y in range(SAFE_Y):
  c=int(y/SAFE_Y*17);d.line((0,y,W,y),fill=(5+c//4,20+c//2,35+c))
 d.rounded_rectangle((42,60,1038,158),radius=26,fill=(12,61,78),outline=(54,151,160),width=2)
 d.text((72,81),'データ照合 / 3ステップ',font=font(47,True),fill='#FFFFFF')
 d.text((72,196),'架空のデモ数値・自動修正ではありません',font=font(32),fill='#B9D8E2')
 d.text((72,276),('① AI下書き' if p==0 else '② 元データ' if p==1 else '③ 差分を確認'),font=font(60,True),fill='#FFFFFF')
 active=(p==0,p==1)
 for i,(x,name,num,color) in enumerate(((58,'AIの下書き',draft,'#F5A8A4'),(556,'元データ',source,'#6EE4D7'))):
  card(d,(x,410,x+466,858),(20,54,75) if i==0 else (15,67,71),color if active[i] else '#547B8A',width=7 if active[i] else 3)
  d.text((x+36,460),name,font=font(45,True),fill='#FFFFFF')
  d.text((x+90,566),num,font=font(166,True),fill=color)
  d.text((x+36,787),'架空の値',font=font(29),fill='#BCD2DB')
 if p==0:detail,note='最初に AI の出力を読む','下書きの数値は 17'
 elif p==1:detail,note='次に 元データと照合','元データの数値は 18'
 else:detail,note='差分を見つけ、人が判断する',f'差分 {abs(int(source)-int(draft))} / 修正は社員が確認'
 card(d,(58,918,1022,1117),(13,81,92),'#54D8D4')
 d.text((90,947),detail,font=font(46,True),fill='#FFFFFF')
 d.text((90,1034),note,font=font(32),fill='#A9F4EA')
 for i in range(3):card(d,(342+i*136,1183,444+i*136,1200),'#66E5DB' if i==p else '#36576B','#36576B',width=1,radius=8)
 card(d,(54,1282,1026,1392),(76,35,49),'#B35B71',width=2)
 d.text((81,1310),'未承認・社員確認後に手動投稿',font=font(36,True),fill='#FFFFFF')
 return img
def cmd(args,log):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 Path(log).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-1200:])
def render(source,out,tmp,genre='ai_work',expected_source_sha=None):
 check(genre,expected_source_sha)
 source=Path(source);out=Path(out);tmp=Path(tmp)
 if not source.is_file():raise FileNotFoundError(source)
 if not expected_source_sha or sha256(source)!=expected_source_sha:raise RuntimeError('FAIL_CLOSED_SOURCE_SHA_MISMATCH')
 tmp.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
 frames=tmp/'private_top_overlays';frames.mkdir(exist_ok=True)
 for n in range(END-START):render_frame(n,genre).save(frames/f'{n:03d}.png',compress_level=1)
 graph=f"[1:v]setpts=PTS+{START}/30/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{START},{END-1})'[v]"
 cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(frames/'%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r','30','-frames:v',str(NFRAMES),'-c:a','copy','-movflags','+faststart',str(out)],tmp/'encode.log')
 report={'policy':POLICY,'genre':genre,'source_sha256':expected_source_sha,'output_sha256':sha256(out),'changed_frames':[START,END-1],'phase_frames':[29,29,29],'source_numbers_are_fictional':True,'real_ui_capture_added':False,'independent_asr':'NOT_VERIFIED','commercial_rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED','publication_allowed':False}
 (tmp/'render_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 return report
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--output',required=True)
 a.add_argument('--tmp',required=True);a.add_argument('--genre',choices=GENRES,default='ai_work')
 a.add_argument('--expected-source-sha',required=True)
 v=a.parse_args();print(json.dumps(render(v.source,v.output,v.tmp,v.genre,v.expected_source_sha),ensure_ascii=False))
