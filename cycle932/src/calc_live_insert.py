#!/usr/bin/env python3
"""cycle932: newly recorded fictional Calc GUI inserted in scene05.

Local private input MP4 and screen capture are never committed. Review only;
not recovered v33, ASR proof, asset clearance, or employee approval.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, END, SAFE_Y = 348, 435, 1460
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRES = {
 'ai_work': ('AI仕事術','#36E1D2'), 'finance': ('家計管理','#79BFFF'),
 'health': ('生活習慣','#99E1B2'), 'travel': ('旅行準備','#A7BDFF'),
 'beauty': ('美容ケア','#E9B0DA'), 'cooking': ('料理・献立','#FFC68B'),
 'education': ('学習効率','#C9B8FF'), 'career': ('仕事・転職','#E9CE85'),
 'lifestyle': ('暮らし','#F0BFCB'), 'technology': ('テクノロジー','#98DFE5')}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def beat(frame):
 if not START <= frame < END: raise ValueError('outside scene05')
 return min(2, 3*(frame-START)//(END-START))

def ensure_contract(genre):
 if genre not in GENRES: raise ValueError('unsupported genre')
 if (END-START)!=87 or SAFE_Y>=1490 or len(GENRES)!=10: raise RuntimeError('unsafe geometry')
 if 'PUBLICATION_NOT_APPROVED' not in POLICY: raise RuntimeError('approval guard missing')

def draw_frame(capture_frame,frame,genre='ai_work'):
 ensure_contract(genre)
 title,accent=GENRES[genre]
 base=Image.new('RGB',(WIDTH,SAFE_Y),'#071626');d=ImageDraw.Draw(base)
 for y in range(SAFE_Y):
  d.line((0,y,WIDTH,y),fill=(8+int(y*5/SAFE_Y),21+int(y*10/SAFE_Y),37+int(y*12/SAFE_Y)))
 d=ImageDraw.Draw(base)
 def ft(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
 def txt(x,y,s,size=36,color='#F2FBFF',bold=False):d.text((x,y),s,font=ft(size,bold),fill=color)
 d.rounded_rectangle((54,44,1026,134),radius=20,fill='#14384A',outline=accent,width=3)
 txt(83,68,title+' / 実操作・架空データ',33,'#EAFBFF',True)
 txt(74,182,'空欄を確認し、',62,'#FFFFFF',True)
 txt(74,274,'表を再計算する',61,accent,True)
 txt(78,361,'LibreOffice Calc を実際に操作して収録',29,'#BED4DD')
 # Only locally recorded fictional A1:C5 workbook pixels are shown.
 crop=capture_frame.crop((0,140,520,445)).resize((942,553),Image.Resampling.LANCZOS)
 d.rounded_rectangle((55,429,1025,1037),radius=27,fill='#0C2D40',outline='#6A99AC',width=4)
 base.paste(crop,(69,471));d=ImageDraw.Draw(base)
 d.rectangle((70,447,1010,471),fill='#0E5267')
 txt(88,440,'CALC / FICTIONAL SCREEN CAPTURE',18,'#E7FFFF',True)
 phase=beat(frame)
 labels=['01  空欄を確認','02  架空の数値を入力','03  合計が再計算される']
 d.rounded_rectangle((70,1090,1010,1230),radius=25,fill='#12465A',outline=accent,width=3)
 txt(105,1122,labels[phase],49,'#FFFFFF',True)
 d.rounded_rectangle((74,1282,1006,1398),radius=22,fill='#552A3D',outline='#FFB1B7',width=3)
 txt(107,1313,'未承認：社員確認後に手動投稿',36,'#FFE7EB',True)
 return base

def run(source,capture,output,workdir,genre='ai_work',expected_source_sha=None):
 source=Path(source);capture=Path(capture);output=Path(output);workdir=Path(workdir)
 ensure_contract(genre)
 for path in (source,capture):
  if not path.is_file():raise FileNotFoundError(path)
 if expected_source_sha and sha256(source)!=expected_source_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 workdir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 extracted=workdir/'capture';extracted.mkdir(exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.60','-i',str(capture),'-t',str((END-START)/FPS),'-vf','fps=30','-frames:v',str(END-START),str(extracted/'%03d.png')]
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('capture extract failed: '+p.stderr[-1000:])
 paths=sorted(extracted.glob('*.png'))
 if len(paths)!=END-START:raise RuntimeError(f'capture frames {len(paths)} != {END-START}')
 overlay=workdir/'overlay';overlay.mkdir(exist_ok=True)
 for i,path in enumerate(paths):
  with Image.open(path) as im: frame=draw_frame(im.convert('RGB'),START+i,genre)
  frame.save(overlay/f'{i:03d}.png',compress_level=1)
 filt=(f'[1:v]setpts=PTS-STARTPTS+{START/FPS}/TB[edit];'
       f'[0:v][edit]overlay=0:0:eof_action=pass:enable=\'between(n,{START},{END-1})\'[v]')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-framerate','30','-start_number','0','-i',str(overlay/'%03d.png'),
      '-filter_complex',filt,'-map','[v]','-map','0:a:0',
      '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
      '-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 (workdir/'ffmpeg.log').write_text(p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('video encode failed: '+p.stderr[-1000:])
 result={'policy':POLICY,'genre':genre,'source_sha256':sha256(source),
         'capture_sha256':sha256(capture),'output_sha256':sha256(output),
         'scene':'05','frames':[START,END-1],'source':'newly recorded fictional Calc GUI',
         'subtitle_safe_y':SAFE_Y,'japanese_asr':'NOT_VERIFIED','rights':'NOT_CLEARED',
         'approval':'NOT_APPROVED','reference_v33':'NOT_AVAILABLE'}
 (workdir/'render_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--source',required=True);ap.add_argument('--capture',required=True)
 ap.add_argument('--output',required=True);ap.add_argument('--workdir',required=True)
 ap.add_argument('--genre',default='ai_work',choices=GENRES)
 ap.add_argument('--expected-source-sha');a=ap.parse_args()
 print(json.dumps(run(a.source,a.capture,a.output,a.workdir,a.genre,a.expected_source_sha),ensure_ascii=False))
