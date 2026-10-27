"""cycle913 review-only: animated attention pointer over original local Calc screenshots.

Source screenshots, voice, and rendered MP4 stay in private review attachments.
This is an editorial annotation, NOT a recording of real mouse activity.
"""
from __future__ import annotations
import argparse
import hashlib
import math
import subprocess
from pathlib import Path

FPS = 30
START = 87
END = 174
W, H = 1080, 1920
SAFE_Y = 1480
POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
ACCENTS = {
 'ai_work': '#48e8ef', 'business': '#8ebaff', 'learning': '#c6a5ff',
 'health': '#6fe0b0', 'beauty': '#ffb3d2', 'travel': '#6ddaff',
 'money': '#9beaac', 'cooking': '#ffc489', 'pets': '#ffe28a',
 'entertainment': '#f4b4ff'
}
# Scene02 stage-specific, source-grounded visual anchors in the 1080x1920 frame.
ANCHORS = ((530, 975), (540, 825), (525, 558))
STARTS = ((870, 1210), (910, 1190), (890, 1020))
LABELS = ('元データの合計', '合計セル B5', 'SUM関数の範囲')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path: Path) -> str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for part in iter(lambda:f.read(1<<20),b''):h.update(part)
 return h.hexdigest()

def stage(i: int) -> int:
 if i<0 or i>=END-START: raise ValueError('frame out of range')
 return i//29

def smooth(t: float) -> float:
 t=max(0.,min(1.,t))
 return t*t*(3-2*t)

def pointer_xy(i: int) -> tuple[float,float]:
 s=stage(i); p=smooth((i%29)/19)
 return tuple(STARTS[s][j]*(1-p)+ANCHORS[s][j]*p for j in (0,1))

def validate(source:Path,output:Path,expected_sha:str,genre:str,policy:str=POLICY):
 if policy!=POLICY: raise ValueError('review-only policy missing')
 if genre not in ACCENTS: raise ValueError('genre not approved')
 if not source.is_file() or sha256(source)!=expected_sha:raise ValueError('source SHA mismatch')
 if source.resolve()==output.resolve():raise ValueError('source overwrite forbidden')
 if not output.name.endswith('REVIEW_ONLY.mp4'):raise ValueError('output must be review-only')
 if any(y>=SAFE_Y or x<0 or x>=W for x,y in (*ANCHORS,*STARTS)):
  raise ValueError('annotation outside subtitle-safe area')

def draw_frames(outdir:Path,genre:str)->None:
 from PIL import Image, ImageDraw, ImageFont
 outdir.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype(FONT,30)
 small=ImageFont.truetype(FONT,23)
 for i in range(END-START):
  s=stage(i); k=i%29; x,y=pointer_xy(i)
  img=Image.new('RGBA',(W,SAFE_Y),(0,0,0,0)); d=ImageDraw.Draw(img)
  accent=ACCENTS[genre]
  # A guided cursor overlay, deliberately labeled as a guide rather than real mouse footage.
  progress=smooth(k/19)
  alpha=int(225*min(1.,k/4,(29-k)/4))
  if alpha>0:
   radius=24+int(7*math.sin(k*.36)**2)
   d.ellipse((x-radius,y-radius,x+radius,y+radius),outline=accent,width=6)
   d.ellipse((x-7,y-7,x+7,y+7),fill='white')
   d.line((x+22,y+22,x+57,y+57),fill=accent,width=6)
   # Reveal the source anchor without hiding original cells/formula.
   box=[(150,924,900,1022),(248,753,836,886),(95,503,954,612)][s]
   if progress>.45:
    d.rounded_rectangle(box,radius=17,outline=accent,width=5)
  d.rounded_rectangle((55,1371,950,1448),radius=17,fill=(5,26,44,230),outline=accent,width=3)
  d.text((82,1387),f'操作ガイド {s+1}/3   {LABELS[s]}',font=font,fill='white')
  d.text((770,1415),'※ 操作再現ではありません',font=small,fill='#d3e7f3',anchor='ra')
  img.save(outdir/f'{i:03d}.png',compress_level=2)

def render(source:Path,output:Path,expected_sha:str,genre:str,frames:Path):
 validate(source,output,expected_sha,genre)
 draw_frames(frames,genre)
 output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-itsoffset',str(START/FPS),'-framerate',str(FPS),'-i',str(frames/'%03d.png'),
      '-filter_complex',f'[0:v][1:v]overlay=0:0:eof_action=pass:shortest=0:format=auto:enable=between(t\\,{START/FPS}\\,{(END-1)/FPS})[v]',
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','21',
      '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 return output

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--expected-sha',required=True)
 p.add_argument('--genre',default='ai_work',choices=sorted(ACCENTS))
 p.add_argument('--frames',type=Path,required=True)
 a=p.parse_args()
 print(render(a.source,a.output,a.expected_sha,a.genre,a.frames))
if __name__=='__main__':main()
