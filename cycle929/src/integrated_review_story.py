#!/usr/bin/env python3
"""Cycle929: review-only, genre-safe scenes 05 and 08; never publishes media.

Input media is private and must be rights-cleared for even internal use. Code
renders only synthetic fictional visual elements and retains inherited audio.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
CAPTION_SAFE_Y = 1460
SCENE5 = (348, 435)  # 11.6 - 14.5 seconds
SCENE8 = (609, 691)  # 20.3 - 23.033 seconds
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
 'ai_work': ('AI仕事術','月次集計','#43DFCF'),
 'finance': ('家計管理','支出の記録','#7CCBFF'),
 'health': ('生活習慣','健康の記録','#9BE3BA'),
 'travel': ('旅行準備','旅程の整理','#A7BBFF'),
 'beauty': ('美容ケア','ケアの記録','#F2B9DA'),
 'cooking': ('料理・献立','献立の作成','#FFC995'),
 'education': ('学習効率','復習の計画','#C8BCFF'),
 'career': ('仕事・転職','面談の準備','#F4D28B'),
 'lifestyle': ('暮らし','家事の分担','#F1BFC7'),
 'technology': ('テクノロジー','設定の確認','#9EE1E8'),
}

def sha256(path: Path) -> str:
 h = hashlib.sha256()
 with open(path, 'rb') as f:
  for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
 return h.hexdigest()

def validate() -> bool:
 assert len(GENRES)==10 and SCENE5[1]-SCENE5[0]==87 and SCENE8[1]-SCENE8[0]==82
 assert CAPTION_SAFE_Y==1460 and FRAMES==691
 assert 'PUBLICATION_NOT_APPROVED' in POLICY
 assert all(len(v)==3 and v[2].startswith('#') and len(v[2])==7 for v in GENRES.values())
 return True

def beat(frame: int, scene: int) -> int:
 start,end = SCENE5 if scene==5 else SCENE8
 if not start <= frame < end: raise ValueError('frame outside scene')
 return min(2, (frame-start)*3//(end-start))

def render(frame: int, scene: int, genre: str='ai_work') -> Image.Image:
 validate()
 if genre not in GENRES: raise ValueError('unknown genre')
 stage=beat(frame,scene)
 title,task,accent=GENRES[genre]
 img=Image.new('RGB',(WIDTH,CAPTION_SAFE_Y),(7,17,34))
 d=ImageDraw.Draw(img)
 for y in range(CAPTION_SAFE_Y):
  d.line((0,y,WIDTH,y),fill=(7+int(8*y/CAPTION_SAFE_Y),17+int(15*y/CAPTION_SAFE_Y),34+int(14*y/CAPTION_SAFE_Y)))
 def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
 def txt(x,y,s,n=34,c='#F4FBFF',b=False):d.text((x,y),s,font=font(n,b),fill=c)
 def box(xy,r=22,fill='#15374A',outline=None,w=2):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
 # The same brand-safe header and disclosure are used for all ten genres.
 box((52,48,1028,140),23,'#12384E','#32677A')
 txt(82,73,title+' / REVIEW ONLY',33,'#E8F9FF',True)
 txt(887,73,f'{scene:02d}/08',29,accent,True)
 if scene==5:
  box((54,170,1026,374),30,'#102C42','#3D6E7C',3)
  txt(91,191,'AIの出力は、まず照合',48,'#FFFFFF',True)
  txt(91,275,'確認できるまで使わない',42,'#F9D08D',True)
  box((751,401,1023,489),19,'#542A38','#F5A2A2',3)
  txt(800,422,'未承認',41,'#FFDBDD',True)
  # 3-stage evidence card: never show a green "approved" tick.
  box((75,519,1005,1118),34,'#F2F8FB','#94B9C8',3)
  txt(111,550,'架空の確認例',32,'#17415A',True)
  txt(112,619,task+'：元データとの照合',39,'#14354C',True)
  steps=[('01','根拠の確認','未確認'),('02','数値の照合','確認対象'),('03','人による最終判断','未実施')]
  for i,(num,label,state) in enumerate(steps):
   y=705+i*122
   active=i==stage
   box((107,y,969,y+101),18,'#D6F1EC' if active else '#E6EFF4',accent if active else '#CBDCE5',4 if active else 1)
   box((127,y+18,198,y+83),14,accent if active else '#9AB5C4')
   txt(142,y+25,num,28,'#123547',True)
   txt(221,y+23,label,35,'#173A4D',True)
   txt(779,y+31,state,27,'#8B4050' if not active else '#146C69',True)
  box((80,1160,1000,1301),23,'#173D52','#3A7180')
  txt(108,1194,'確認が終わるまで投稿しない',41,'#FFFFFF',True)
  txt(82,1364,'FICTIONAL DATA / EMPLOYEE REVIEW REQUIRED',25,'#B6D1D9')
 else:
  box((58,176,1022,361),31,'#123147','#357181',3)
  txt(91,199,'小さな時短を、毎日の習慣に',46,'#FFFFFF',True)
  txt(93,281,'使う前に、1つだけ確認する',38,accent,True)
  box((62,409,1018,1020),33,'#EAF3F7','#83AAB9',3)
  txt(102,443,'TODAY’S 3-STEP CHECK',33,'#1A455D',True)
  steps=[('1','元データを見る'),('2','差分を修正する'),('3','社員が承認を判断')]
  for i,(num,lab) in enumerate(steps):
   y=529+i*151
   active=i==stage
   box((102,y,975,y+124),24,'#D3F0EB' if active else '#F9FCFE',accent if active else '#C6D7DF',5 if active else 2)
   box((125,y+25,208,y+103),20,accent if active else '#A7C0CB')
   txt(151,y+36,num,36,'#153E52',True)
   txt(247,y+33,lab,41,'#173B4E',True)
   if active: txt(899,y+34,'→',42,'#1A7E7D',True)
  box((69,1055,1011,1227),28,'#4B2A3B','#F0A6AE',3)
  txt(106,1082,'公開ステータス：未承認',41,'#FFE6E8',True)
  txt(107,1151,'投稿は社員承認後、手動のみ',31,'#FFE6E8',True)
  txt(78,1355,'DEMO ONLY / NOT APPROVED FOR PUBLICATION',24,'#C0D9E1')
 # Entire y >= 1460 untouched to preserve the burned captions.
 return img

def encode(source:Path,output:Path,workdir:Path,genre:str):
 workdir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 for scene,(start,end) in [(5,SCENE5),(8,SCENE8)]:
  folder=workdir/f'scene{scene}';folder.mkdir(exist_ok=True)
  for i,frame in enumerate(range(start,end)):
   render(frame,scene,genre).save(folder/f'{i:03d}.png',compress_level=1)
 filt=(f'[1:v]setpts=PTS-STARTPTS+{SCENE5[0]/FPS}/TB[s5];'
       f'[2:v]setpts=PTS-STARTPTS+{SCENE8[0]/FPS}/TB[s8];'
       f'[0:v][s5]overlay=0:0:eof_action=pass:enable=\'between(t,{SCENE5[0]/FPS},{(SCENE5[1]-1)/FPS})\'[v5];'
       f'[v5][s8]overlay=0:0:eof_action=pass:enable=\'between(t,{SCENE8[0]/FPS},{(SCENE8[1]-1)/FPS})\'[v]')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(workdir/'scene5'/'%03d.png'),'-framerate','30','-start_number','0','-i',str(workdir/'scene8'/'%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
 proc=subprocess.run(cmd,capture_output=True,text=True)
 (workdir/'ffmpeg.log').write_text(proc.stderr,encoding='utf-8')
 if proc.returncode:raise RuntimeError(f'ffmpeg failed {proc.returncode}: {proc.stderr[-1000:]}')
 return {'policy':POLICY,'genre':genre,'source_sha256':sha256(source),'output_sha256':sha256(output),'changed_scenes':[5,8],'caption_safe_y':CAPTION_SAFE_Y,'audio_content_semantics':'NOT_INDEPENDENTLY_VERIFIED','reference':'original v33 unavailable; reimplementation'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--workdir',type=Path,required=True);p.add_argument('--genre',choices=GENRES,default='ai_work');p.add_argument('--expected-source-sha',default=None);a=p.parse_args()
 if a.expected_source_sha and sha256(a.source)!=a.expected_source_sha:raise ValueError('private source hash mismatch')
 report=encode(a.source,a.output,a.workdir,a.genre)
 (a.workdir/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
