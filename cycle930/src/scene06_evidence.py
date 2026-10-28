#!/usr/bin/env python3
"""cycle930: fictional evidence comparison in scene 06; review-only.

Private inherited MP4 is never uploaded to GitHub. This reimplementation
preserves source AAC and burned-in captions; it does NOT independently ASR
transcribe the Japanese narration or approve publication.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, END, CAPTION_SAFE_Y = 435, 522, 1460
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRES = {
 'ai_work': ('AI仕事術', '#43DFCF'), 'finance': ('家計管理', '#7CCBFF'),
 'health': ('生活習慣', '#9BE3BA'), 'travel': ('旅行準備', '#A7BBFF'),
 'beauty': ('美容ケア', '#F2B9DA'), 'cooking': ('料理・献立', '#FFC995'),
 'education': ('学習効率', '#C8BCFF'), 'career': ('仕事・転職', '#F4D28B'),
 'lifestyle': ('暮らし', '#F1BFC7'), 'technology': ('テクノロジー', '#9EE1E8')}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def stage(frame):
 if not START <= frame < END:raise ValueError('out of scene')
 return min(2,(frame-START)*3//(END-START))

def validate():
 assert END-START==87 and FRAMES==691 and CAPTION_SAFE_Y==1460
 assert len(GENRES)==10 and 'PUBLICATION_NOT_APPROVED' in POLICY
 return True

def render(frame, genre='ai_work'):
 validate()
 if genre not in GENRES:raise ValueError('unknown genre')
 label,accent=GENRES[genre]; s=stage(frame); local=frame-START
 im=Image.new('RGB',(WIDTH,CAPTION_SAFE_Y)); px=im.load()
 # Original, synthetic dark editorial gradient (no imported people, logos or data).
 for y in range(CAPTION_SAFE_Y):
  base=(8+int(10*y/CAPTION_SAFE_Y),18+int(18*y/CAPTION_SAFE_Y),34+int(20*y/CAPTION_SAFE_Y))
  ImageDraw.Draw(im).line((0,y,WIDTH,y),fill=base)
 d=ImageDraw.Draw(im)
 def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
 def txt(x,y,t,size=36,color='#F5FAFF',bold=False):d.text((x,y),t,font=font(size,bold),fill=color)
 def card(xy,fill,outline='#3D687B',r=25,w=3):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
 # Stable margins, no overlap with the existing caption zone y>=1460.
 card((50,48,1030,142),'#12374A','#3B7081',22)
 txt(80,76,label+' / REVIEW ONLY',31,'#E9F8FF',True)
 txt(888,77,'06/08',29,accent,True)
 txt(75,194,'違いを見つけたら、',57,'#FFFFFF',True)
 txt(75,275,'根拠を見て修正する',54,accent,True)
 txt(78,359,'架空の数値例 / 実際の売上ではありません',27,'#B8CBD7')
 left=(68,460,520,911); right=(560,460,1012,911)
 active=(local%29)/28.0
 card(left,'#173248', '#F6B56C' if s==0 else '#466C7C',28,5 if s==0 else 2)
 card(right,'#16364A',accent if s>=1 else '#466C7C',28,5 if s>=1 else 2)
 txt(104,505,'AIの下書き',38,'#E4F2FC',True)
 txt(600,505,'元データ',38,'#E4F2FC',True)
 txt(121,604,'17',142,'#FFB6A4',True)
 txt(619,604,'18',142,accent,True)
 txt(110,809,'確認前の値',29,'#B8C9D4')
 txt(608,809,'照合する値',29,'#B8C9D4')
 cy=1005
 d.line((95,cy,985,cy),fill='#406276',width=9)
 cx=round(95+890*(local+1)/87)
 d.ellipse((cx-12,cy-12,cx+12,cy+12),fill=accent)
 phases=['01  差分を発見','02  元データと照合','03  修正案を確認']
 card((72,1063,1008,1245),'#123A50',accent,27,3)
 txt(110,1102,phases[s],49,'#FFFFFF',True)
 if s==0: note='下書きと元データが違う'
 elif s==1: note='推測で値を埋めない'
 else: note='修正後も社員が最終確認'
 txt(110,1181,note,29,'#BDE9E4')
 card((75,1281,1005,1396),'#4A2B3A','#EAA1AB',24,3)
 txt(108,1311,'未承認：社員確認まで投稿しない',36,'#FFE4E6',True)
 return im

def encode(source,output,workdir,genre='ai_work',expected_source_sha=None):
 source=Path(source);output=Path(output);workdir=Path(workdir)
 if not source.is_file():raise FileNotFoundError(source)
 if expected_source_sha and sha256(source)!=expected_source_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 if genre not in GENRES:raise ValueError('unknown genre')
 workdir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 for f in range(START,END):render(f,genre).save(workdir/f'{f-START:03d}.png',compress_level=1)
 filt=(f'[1:v]setpts=PTS-STARTPTS+{START/FPS}/TB[edit];'
       f'[0:v][edit]overlay=0:0:eof_action=pass:enable=\'between(n,{START},{END-1})\'[v]')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-framerate','30','-start_number','0','-i',str(workdir/'%03d.png'),
      '-filter_complex',filt,'-map','[v]','-map','0:a:0',
      '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
      '-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 (workdir/'ffmpeg.log').write_text(p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-2000:])
 result={'policy':POLICY,'genre':genre,'source_sha256':sha256(source),
         'output_sha256':sha256(output),'changed_frames':[START,END-1],
         'subtitle_safe_y':CAPTION_SAFE_Y,'japanese_asr':'NOT_VERIFIED',
         'reference':'16-panel storyboard; v33 original unavailable',
         'rights':'NOT_CLEARED','approval':'NOT_APPROVED'}
 (workdir/'render_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--workdir',required=True);p.add_argument('--genre',choices=GENRES,default='ai_work')
 p.add_argument('--expected-source-sha');a=p.parse_args()
 print(json.dumps(encode(a.source,a.output,a.workdir,a.genre,a.expected_source_sha),ensure_ascii=False))
