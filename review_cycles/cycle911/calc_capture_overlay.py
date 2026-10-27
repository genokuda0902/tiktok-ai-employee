"""Cycle911: real local LibreOffice Calc screenshot inset, review-only."""
from __future__ import annotations
import argparse
import hashlib
import subprocess
from pathlib import Path

FPS=30
START_FRAME=87
END_FRAME=174
VIDEO_W,VIDEO_H=1080,1920
OVERLAY_Y,OVERLAY_H=230,1200
CAPTION_SAFE_Y=1490
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRE_ACCENTS={
 'ai_work':'#33d4e8','business':'#67a8ff','learning':'#b28cff',
 'health':'#50ddad','beauty':'#ff98c8','travel':'#4ac6ed',
 'money':'#7bdf9a','cooking':'#ffb15a','pets':'#f8ce6b',
 'entertainment':'#d7a2ff'
}
STAGES=('① 3か月分の表を確認','② 合計セル B5 を選択','③ SUM関数を画面で確認')

def sha256(path:Path)->str:
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def validate(source:Path,output:Path,screenshots:list[Path],expected_sha:str,genre:str):
 if genre not in GENRE_ACCENTS:raise ValueError('unapproved genre')
 if not output.name.endswith('REVIEW_ONLY.mp4'):raise ValueError('publication guard')
 if source.resolve()==output.resolve():raise ValueError('source must not be overwritten')
 if sha256(source)!=expected_sha:raise ValueError('source SHA256 mismatch')
 if len(screenshots)!=3 or not all(p.is_file() for p in screenshots):
  raise ValueError('three real local Calc captures required')
 if OVERLAY_Y+OVERLAY_H>=CAPTION_SAFE_Y:raise ValueError('caption safe area')

def make_overlay_frames(screenshots:list[Path],dest:Path,genre:str):
 from PIL import Image,ImageDraw,ImageFont
 dest.mkdir(parents=True,exist_ok=True)
 bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
 regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 def font(n,b=True):return ImageFont.truetype(bold if b else regular,n)
 def screenshot(p):
  im=Image.open(p).convert('RGB').crop((57,51,785,600))
  return im.resize((972,734),Image.Resampling.LANCZOS)
 imgs=[screenshot(p) for p in screenshots]
 accent=GENRE_ACCENTS[genre]
 for i in range(END_FRAME-START_FRAME):
  stage=min(2,i//29)
  im=Image.new('RGBA',(VIDEO_W,OVERLAY_H),(0,0,0,0));d=ImageDraw.Draw(im)
  d.rounded_rectangle((25,5,1055,1180),radius=30,fill=(5,20,40,251),outline=accent,width=4)
  d.text((58,36),'実際の表計算画面で確認',font=font(51),fill='white')
  d.text((58,114),'LibreOffice Calc｜架空データ｜ローカル実演',font=font(26,False),fill='#c7e7f2')
  d.rounded_rectangle((48,207,1032,961),radius=18,fill='#dceaf0')
  crop=imgs[stage]
  scale=1.0+.007*((i%29)/28)
  if scale>1:
   nw,nh=int(crop.width*scale),int(crop.height*scale)
   crop=crop.resize((nw,nh),Image.Resampling.BICUBIC)
   cx,cy=(nw-972)//2,(nh-734)//2
   crop=crop.crop((cx,cy,cx+972,cy+734))
  im.alpha_composite(crop.convert('RGBA'),(54,215))
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((60,984,1020,1072),radius=18,fill=(12,54,77,255))
  d.text((82,1001),STAGES[stage],font=font(37),fill=accent)
  for j in range(3):
   d.rounded_rectangle((65+j*322,1094,365+j*322,1109),radius=6,
    fill=accent if j<=stage else '#34506a')
  d.text((62,1131),'自作の架空データです。Excelの画面ではありません。',
   font=font(22,False),fill='#c8d9e7')
  im.save(dest/f'{i:03d}.png',compress_level=3)
 return END_FRAME-START_FRAME

def render(source:Path,output:Path,screenshots:list[Path],expected_sha:str,
           genre:str,frames_dir:Path):
 validate(source,output,screenshots,expected_sha,genre)
 make_overlay_frames(screenshots,frames_dir,genre)
 output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
  '-i',str(source),'-itsoffset',str(START_FRAME/FPS),'-framerate',str(FPS),
  '-i',str(frames_dir/'%03d.png'),
  '-filter_complex',
  f'[0:v][1:v]overlay=x=0:y={OVERLAY_Y}:eof_action=pass:shortest=0:format=auto:enable=between(t\\,{START_FRAME/FPS}\\,{(END_FRAME-1)/FPS})[v]',
  '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast',
  '-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
  '-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 return output

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--source',required=True,type=Path)
 ap.add_argument('--output',required=True,type=Path)
 ap.add_argument('--expected-sha',required=True)
 ap.add_argument('--genre',default='ai_work',choices=sorted(GENRE_ACCENTS))
 ap.add_argument('--captures',nargs=3,required=True,type=Path)
 ap.add_argument('--frames-dir',required=True,type=Path)
 a=ap.parse_args()
 print(render(a.source,a.output,a.captures,a.expected_sha,a.genre,a.frames_dir))

if __name__=='__main__':main()
