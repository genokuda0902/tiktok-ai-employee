"""cycle912: source-grounded Calc magnification for a private, review-only MP4.

No screenshots, voice or finished MP4 are committed to public GitHub.
This is a reimplementation, not recovered v33 code or a transcript validator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

FPS=30
START_FRAME=87
END_FRAME=174
VIDEO_W=1080
OVERLAY_Y=230
OVERLAY_H=1200
CAPTION_SAFE_Y=1490
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRE_ACCENTS={
 'ai_work':'#3ce2f2','business':'#6ba8ff','learning':'#b9a0ff',
 'health':'#64ddaa','beauty':'#ff9fcb','travel':'#64d3ff',
 'money':'#8de4a3','cooking':'#ffbb72','pets':'#ffd37a',
 'entertainment':'#e4a5ff'
}
STAGES=('元データの数値を確認','合計セル B5 を拡大','SUM関数の参照範囲を確認')

def sha256(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def stage_for_frame(i:int)->int:
 if not 0<=i<END_FRAME-START_FRAME:raise ValueError('frame out of range')
 return min(2,i//29)

def check_policy(source:Path,output:Path,captures:list[Path],expected_sha:str,genre:str,policy:str=POLICY):
 if policy!=POLICY:raise ValueError('missing review-only policy')
 if genre not in GENRE_ACCENTS:raise ValueError('genre not allowlisted')
 if source.resolve()==output.resolve():raise ValueError('source overwrite forbidden')
 if output.suffix.lower()!='.mp4' or not output.name.endswith('REVIEW_ONLY.mp4'):
  raise ValueError('output must be REVIEW_ONLY.mp4')
 if not source.is_file() or sha256(source)!=expected_sha:raise ValueError('source SHA mismatch')
 if len(captures)!=3 or any(not p.is_file() for p in captures):raise ValueError('three local screenshots required')
 if OVERLAY_Y+OVERLAY_H>=CAPTION_SAFE_Y:raise ValueError('caption overlap')

def create_frames(captures:list[Path],dest:Path,genre:str):
 from PIL import Image,ImageDraw,ImageFont
 dest.mkdir(parents=True,exist_ok=True)
 bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
 regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 fb=lambda n:ImageFont.truetype(bold,n)
 fr=lambda n:ImageFont.truetype(regular,n)
 imgs=[Image.open(p).convert('RGB') for p in captures]
 accent=GENRE_ACCENTS[genre]
 def crop(img,rect,size):return img.crop(rect).resize(size,Image.Resampling.LANCZOS)
 # Pixel-backed crops: no invented GUI. Formula and totals come from real local Calc captures.
 table=crop(imgs[0],(88,215,717,507),(932,430))
 totals=crop(imgs[1],(86,393,719,507),(930,168))
 b5=crop(imgs[1],(222,430,402,504),(860,350))
 formula=crop(imgs[2],(312,151,815,195),(942,115))
 range_cells=crop(imgs[2],(225,270,398,506),(520,580))
 for i in range(END_FRAME-START_FRAME):
  stage=stage_for_frame(i)
  local=i%29
  canvas=Image.new('RGBA',(VIDEO_W,OVERLAY_H),(0,0,0,0))
  d=ImageDraw.Draw(canvas)
  d.rounded_rectangle((20,6,1060,1185),radius=30,fill=(5,20,38,255),outline=accent,width=4)
  d.text((55,34),'実際の表計算を拡大して確認',font=fb(45),fill='white')
  d.text((55,110),'LibreOffice Calc｜自作の架空データ',font=fr(26),fill='#d1eaf2')
  d.rounded_rectangle((44,170,1036,972),radius=20,fill='#e5eef4')
  if stage==0:
   canvas.alpha_composite(table.convert('RGBA'),(74,235))
   canvas.alpha_composite(totals.convert('RGBA'),(75,705))
   d=ImageDraw.Draw(canvas)
   d.text((85,185),'4月・5月・6月の数値と合計',font=fb(31),fill='#0a2944')
  elif stage==1:
   d=ImageDraw.Draw(canvas)
   d.text((85,185),'選択したセルの値を読み取る',font=fb(32),fill='#0a2944')
   canvas.alpha_composite(b5.convert('RGBA'),(112,306))
   d=ImageDraw.Draw(canvas)
   d.rounded_rectangle((122,713,954,842),radius=16,fill='#103a55')
   d.text((150,738),'B5 の表示値：46（架空データ）',font=fb(37),fill='white')
  else:
   d=ImageDraw.Draw(canvas)
   d.text((80,185),'数式バーと参照範囲を照合',font=fb(31),fill='#0a2944')
   canvas.alpha_composite(formula.convert('RGBA'),(68,259))
   canvas.alpha_composite(range_cells.convert('RGBA'),(286,397))
   d=ImageDraw.Draw(canvas)
   d.rounded_rectangle((80,830,1000,918),radius=16,fill='#103a55')
   d.text((109,844),'=SUM(B2:B4)  →  12 + 16 + 18 = 46',font=fb(31),fill='white')
  d=ImageDraw.Draw(canvas)
  d.rounded_rectangle((50,988,1030,1074),radius=16,fill=(11,55,78,255))
  d.text((76,1007),STAGES[stage],font=fb(37),fill=accent)
  for j in range(3):
   d.rounded_rectangle((63+j*323,1091,371+j*323,1107),radius=7,fill=accent if j<=stage else '#35556b')
  d.text((61,1130),'※ 実データ・実績ではありません／社員確認前・投稿禁止',font=fr(22),fill='#d4e7ef')
  canvas.save(dest/f'{i:03d}.png',compress_level=2)
 return END_FRAME-START_FRAME

def render(source:Path,output:Path,captures:list[Path],expected_sha:str,genre:str,frames_dir:Path):
 check_policy(source,output,captures,expected_sha,genre)
 create_frames(captures,frames_dir,genre)
 output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-itsoffset',str(START_FRAME/FPS),'-framerate',str(FPS),'-i',str(frames_dir/'%03d.png'),
      '-filter_complex',f'[0:v][1:v]overlay=x=0:y={OVERLAY_Y}:eof_action=pass:shortest=0:format=auto:enable=between(t\\,{START_FRAME/FPS}\\,{(END_FRAME-1)/FPS})[v]',
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','21',
      '-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 return output

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True,type=Path)
 p.add_argument('--output',required=True,type=Path)
 p.add_argument('--expected-sha',required=True)
 p.add_argument('--genre',default='ai_work',choices=sorted(GENRE_ACCENTS))
 p.add_argument('--captures',required=True,nargs=3,type=Path)
 p.add_argument('--frames-dir',required=True,type=Path)
 a=p.parse_args()
 print(render(a.source,a.output,a.captures,a.expected_sha,a.genre,a.frames_dir))
if __name__=='__main__':main()
