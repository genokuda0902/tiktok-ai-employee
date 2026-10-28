#!/usr/bin/env python3
"""cycle933: magnify pixels from an actual fictional Calc GUI source MP4.

Private input/output media must never be committed. Reimplementation only.
Japanese ASR, source rights and employee publication approval remain unverified.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, END, SAFE_Y = 348, 435, 1260
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRES = {
 'ai_work': ('AI仕事術','#36E1D2'), 'finance': ('家計管理','#79BFFF'),
 'health': ('生活習慣','#99E1B2'), 'travel': ('旅行準備','#A7BDFF'),
 'beauty': ('美容ケア','#E9B0DA'), 'cooking': ('料理・献立','#FFC68B'),
 'education': ('学習効率','#C9B8FF'), 'career': ('仕事・転職','#E9CE85'),
 'lifestyle': ('暮らし','#F0BFCB'), 'technology': ('テクノロジー','#98DFE5')}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
CELL_B4 = (397, 748, 677, 816)
CELL_B5 = (397, 818, 677, 893)
LENS_SOURCE = (394, 736, 696, 899)
LENS_TARGET = (535, 914, 991, 1178)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
 return h.hexdigest()

def phase(frame):
 if not START <= frame < END: raise ValueError('outside scene05')
 return min(2,3*(frame-START)//(END-START))

def ensure_contract(genre):
 if genre not in GENRES: raise ValueError('unsupported genre')
 if len(GENRES)!=10 or END-START!=87 or SAFE_Y>=1280:
  raise RuntimeError('unsafe timing or caption geometry')
 if not (0<=LENS_SOURCE[0]<LENS_SOURCE[2]<=WIDTH and 0<=LENS_SOURCE[1]<LENS_SOURCE[3]<SAFE_Y):
  raise RuntimeError('unsafe source crop')
 if LENS_TARGET[3]>=SAFE_Y or 'PUBLICATION_NOT_APPROVED' not in POLICY:
  raise RuntimeError('publication/caption guard')

def font(size,bold=False):
 return ImageFont.truetype(BOLD if bold else FONT,size)

def build_overlay(source_frame,frame,genre='ai_work'):
 """Transparent overlay; the inset comes from real source_frame pixels."""
 ensure_contract(genre)
 if source_frame.size!=(WIDTH,HEIGHT): raise ValueError('unexpected source geometry')
 p=phase(frame); title,accent=GENRES[genre]
 overlay=Image.new('RGBA',(WIDTH,SAFE_Y),(0,0,0,0))
 d=ImageDraw.Draw(overlay)
 target=CELL_B5 if p==2 else CELL_B4
 d.rounded_rectangle((target[0]-7,target[1]-7,target[2]+7,target[3]+7),
                     radius=12,outline=accent,width=7)
 d.rounded_rectangle((50,895,1026,1236),radius=27,fill='#071B2DF8',
                     outline='#6F99A8',width=3)
 d.text((83,926),['01  空欄を確認','02  数値を入力','03  合計を照合'][p],
        font=font(39,True),fill='#FFFFFF')
 d.text((85,991),'実画面のセルを',font=font(27),fill='#B6D2DE')
 d.text((85,1034),'拡大して確認',font=font(29,True),fill=accent)
 d.text((86,1167),'架空データ・実画面から拡大',font=font(24,True),fill='#C8DCE8')
 crop=source_frame.crop(LENS_SOURCE).resize(
     (LENS_TARGET[2]-LENS_TARGET[0],LENS_TARGET[3]-LENS_TARGET[1]),
     Image.Resampling.LANCZOS)
 overlay.paste(crop.convert('RGBA'),LENS_TARGET[:2])
 d=ImageDraw.Draw(overlay)
 d.rounded_rectangle((LENS_TARGET[0]-4,LENS_TARGET[1]-4,
                      LENS_TARGET[2]+4,LENS_TARGET[3]+4),
                     radius=9,outline=accent,width=5)
 d.rounded_rectangle((LENS_TARGET[0]+8,LENS_TARGET[1]+7,
                      LENS_TARGET[0]+182,LENS_TARGET[1]+41),
                     radius=8,fill='#0C3548')
 d.text((LENS_TARGET[0]+19,LENS_TARGET[1]+9),'実画面 × 拡大',
        font=font(19,True),fill='#FFFFFF')
 return overlay

def cmd_run(cmd,log):
 p=subprocess.run(cmd,text=True,capture_output=True)
 Path(log).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError(f'command failed {p.returncode}: '+p.stderr[-1200:])

def run(source,output,workdir,genre='ai_work',expected_source_sha=None):
 source=Path(source);output=Path(output);workdir=Path(workdir)
 ensure_contract(genre)
 if not source.is_file():raise FileNotFoundError(source)
 digest=sha256(source)
 if expected_source_sha and digest!=expected_source_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 output.parent.mkdir(parents=True,exist_ok=True)
 frames=workdir/'source_frames'; frames.mkdir(parents=True,exist_ok=True)
 overlays=workdir/'overlays'; overlays.mkdir(parents=True,exist_ok=True)
 cmd_run(['ffmpeg','-hide_banner','-loglevel','error','-y',
          '-ss',str(START/FPS),'-i',str(source),'-t',str((END-START)/FPS),
          '-vf','fps=30','-frames:v',str(END-START),str(frames/'%03d.png')],
         workdir/'extract.log')
 paths=sorted(frames.glob('*.png'))
 if len(paths)!=END-START:raise RuntimeError('WRONG_FRAME_COUNT')
 for i,path in enumerate(paths):
  with Image.open(path) as im:
   result=build_overlay(im.convert('RGB'),START+i,genre)
  result.save(overlays/f'{i:03d}.png',compress_level=1)
 filtergraph=(f'[1:v]setpts=PTS-STARTPTS+{START/FPS}/TB[edit];'
              f'[0:v][edit]overlay=0:0:eof_action=pass:enable=\'between(n,{START},{END-1})\'[v]')
 cmd_run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-framerate','30','-start_number','0','-i',str(overlays/'%03d.png'),
          '-filter_complex',filtergraph,'-map','[v]','-map','0:a:0',
          '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
          '-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',
          str(output)],workdir/'encode.log')
 info={'policy':POLICY,'genre':genre,'source_sha256':digest,
       'output_sha256':sha256(output),'changed_scene':[START,END-1],
       'original_pixels':'crop from source video, no invented cell values',
       'subtitle_protected_from_y':SAFE_Y,
       'independent_japanese_asr':'NOT_VERIFIED','rights':'NOT_CLEARED',
       'employee_approval':'NOT_APPROVED','phone_playback':'NOT_VERIFIED'}
 (workdir/'render_result.json').write_text(
     json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
 return info

if __name__=='__main__':
 a=argparse.ArgumentParser()
 a.add_argument('--source',required=True);a.add_argument('--output',required=True)
 a.add_argument('--workdir',required=True)
 a.add_argument('--genre',choices=GENRES,default='ai_work')
 a.add_argument('--expected-source-sha')
 v=a.parse_args()
 print(json.dumps(run(v.source,v.output,v.workdir,v.genre,v.expected_source_sha),
                  ensure_ascii=False))
