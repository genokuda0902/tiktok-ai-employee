#!/usr/bin/env python3
"""Review-only: original animated qualitative Before/After hook, 10 genres.

No private video/audio is committed. The narration is inherited, not ASR-verified.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
HOOK_FRAMES, SAFE_Y = 87, 1450
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# Each preset communicates a question and a check, NOT a guaranteed performance result.
GENRES = {
 'ai_work': ('AI仕事術', 'まだ手作業？', '空欄を見つける', '確認までが時短', '月次集計を見直す'),
 'finance': ('家計管理', '支出が見えない？', '項目を整理する', '使い道を確認', '家計の項目を見直す'),
 'health': ('生活習慣', '習慣が続かない？', '一つに絞る', '記録して確認', '今日の習慣を見直す'),
 'travel': ('旅行準備', '準備が不安？', '持ち物を整理', '出発前に確認', '旅の持ち物を見直す'),
 'beauty': ('美容ケア', '何から始める？', '手順を整理する', '使い方を確認', 'ケアの手順を見直す'),
 'cooking': ('料理・献立', '献立に迷う？', '材料を整理する', '手順を確認', '冷蔵庫の材料を見直す'),
 'education': ('学習効率', '勉強が進まない？', '範囲を一つ選ぶ', '理解度を確認', '学習内容を見直す'),
 'career': ('仕事・転職', '準備が進まない？', '経験を整理する', '応募前に確認', '経歴の項目を見直す'),
 'lifestyle': ('暮らし', '片づけに迷う？', '場所を一つ選ぶ', '順番を確認', '家事の手順を見直す'),
 'technology': ('テクノロジー', '設定が難しい？', '項目を整理する', '動作を確認', '設定項目を見直す'),
}
ACCENT = '#38DFD6'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()

def ensure_contract(genre):
 if genre not in GENRES: raise ValueError('unsupported genre')
 if len(GENRES)!=10 or HOOK_FRAMES!=87 or not (0<SAFE_Y<1490):
  raise RuntimeError('unsafe frame geometry')
 if 'PUBLICATION_NOT_APPROVED' not in POLICY: raise RuntimeError('publication guard missing')
 if not Path(BOLD).exists(): raise FileNotFoundError('Japanese font missing')

def font(size,bold=False):
 return ImageFont.truetype(BOLD if bold else FONT,size)

def phase(frame):
 if not 0<=frame<HOOK_FRAMES:raise ValueError('frame outside hook')
 return 0 if frame<24 else 1 if frame<53 else 2

def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)

def draw_center(draw,y,text,size,color='#FFFFFF',bold=True):
 f=font(size,bold)
 b=draw.textbbox((0,0),text,font=f)
 w=b[2]-b[0]
 if w>980:raise ValueError('hook text too wide')
 draw.text(((WIDTH-w)//2,y),text,font=f,fill=color,stroke_width=1 if bold else 0,stroke_fill='#0C2336')

def draw_hook(frame,genre='ai_work'):
 ensure_contract(genre)
 p=phase(frame); label,q,mid,after,detail=GENRES[genre]
 im=Image.new('RGBA',(WIDTH,SAFE_Y),(0,0,0,0))
 d=ImageDraw.Draw(im)
 # Replace only visual content above subtitle band; retain source header and narration.
 d.rectangle((0,120,WIDTH,SAFE_Y),fill=(5,22,39,248))
 for j in range(12):
  y=145+j*83
  d.line((0,y,WIDTH,y-140),fill=(13,49,68,110),width=2)
 titles=[q,mid,after]
 draw_center(d,293,titles[p],93 if len(titles[p])<=8 else 77,'#FFFFFF')
 draw_center(d,435,detail,39,'#B8DAE4',False)
 # Qualitative comparison, no invented numeric results.
 d.rounded_rectangle((64,595,1016,1118),radius=35,fill=(12,41,62,255),outline=(74,117,139,255),width=4)
 d.rounded_rectangle((88,624,505,1049),radius=25,fill=(60,35,48,255),outline=(207,107,111,255),width=4)
 d.text((116,655),'BEFORE',font=font(40,True),fill='#FFB8B9')
 d.text((120,750),'気づかず',font=font(52,True),fill='#FFFFFF')
 d.text((120,835),'進める',font=font(52,True),fill='#FFFFFF')
 d.text((118,968),'確認不足',font=font(28,True),fill='#F7C5C5')
 d.rounded_rectangle((568,624,990,1049),radius=25,fill=(13,67,78,255),outline=(62,220,210,255),width=4)
 d.text((597,655),'AFTER',font=font(40,True),fill='#8CF4E9')
 d.text((597,750),'一つずつ',font=font(51,True),fill='#FFFFFF')
 d.text((597,835),'照合する',font=font(51,True),fill='#FFFFFF')
 d.text((596,968),'確認して使う',font=font(28,True),fill='#B1EDE8')
 reveal=ease((frame-16)/45)
 x=int(568+422*reveal)
 d.rectangle((x,627,988,1047),fill=(7,28,42,246)) if x<988 else None
 d.rounded_rectangle((490,797,583,878),radius=18,fill=(246,252,252,255))
 d.text((506,802),'→',font=font(58,True),fill='#15485A')
 d.rounded_rectangle((85,1140,995,1210),radius=18,fill=(11,71,82,255))
 d.text((130,1154),'結果を決めつけず、元データで確認',font=font(32,True),fill='#E1F6F5')
 d.text((160,1325),'※ 架空例・未承認・社員確認後に手動投稿',font=font(30,True),fill='#B5CDD6')
 for i in range(3):
  d.rounded_rectangle((385+i*112,541,473+i*112,551),radius=5,
                      fill='#3EDDD0' if i<=p else '#315263')
 return im

def cmd(cmd,log):
 p=subprocess.run(cmd,capture_output=True,text=True)
 Path(log).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError(f'command failed {p.returncode}: {p.stderr[-1000:]}')

def render(source,output,workdir,genre='ai_work',expected_source_sha=None):
 ensure_contract(genre)
 source=Path(source);output=Path(output);workdir=Path(workdir)
 if not source.is_file():raise FileNotFoundError(source)
 digest=sha256(source)
 if expected_source_sha and digest!=expected_source_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 workdir.mkdir(parents=True,exist_ok=True); output.parent.mkdir(parents=True,exist_ok=True)
 overlay_dir=workdir/'overlays';overlay_dir.mkdir(exist_ok=True)
 for f in range(HOOK_FRAMES):draw_hook(f,genre).save(overlay_dir/f'{f:03d}.png',compress_level=1)
 graph="[0:v][1:v]overlay=0:0:eof_action=pass:enable='between(n,0,86)'[v]"
 cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-framerate','30','-start_number','0','-i',str(overlay_dir/'%03d.png'),
      '-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264',
      '-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30',
      '-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)],workdir/'encode.log')
 result={'policy':POLICY,'genre':genre,'source_sha256':digest,'output_sha256':sha256(output),
         'changed_frames':[0,86],'subtitle_safe_y':SAFE_Y,'original_japanese_narration':'INHERITED_NOT_ASR_VERIFIED',
         'reference_v33_mp4':'NOT_AVAILABLE','employee_approval':'NOT_APPROVED',
         'assets':'Pillow-original shapes, inherited private MP4, no third-party download'}
 (workdir/'render_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser()
 a.add_argument('--source',required=True);a.add_argument('--output',required=True)
 a.add_argument('--workdir',required=True);a.add_argument('--genre',choices=GENRES,default='ai_work')
 a.add_argument('--expected-source-sha')
 args=a.parse_args()
 print(json.dumps(render(args.source,args.output,args.workdir,args.genre,args.expected_source_sha),ensure_ascii=False))
