#!/usr/bin/env python3
"""Cycle936: original, review-only three-beat prompt typing overlay for scene04.

No private media is stored in GitHub. Simulated typing, NOT ChatGPT screen capture.
10 genre-neutral prompts; publication is denied until employee review.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
SCENE_START, SCENE_END = 261, 348  # 8.7–11.6 seconds; end exclusive
SAFE_Y = 1450
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# All examples are fictional, do not promise measured outcomes or assert a real app recording.
GENRES = {
 'ai_work': ('3か月の売上を整理', '元データだけを使う', '表と要点3つ'),
 'finance': ('家計の支出を整理', '記録した支出だけ使う', '項目別の一覧'),
 'health': ('生活習慣を整理', '自分の記録だけ使う', '確認項目の一覧'),
 'travel': ('旅行準備を整理', '行き先と日程を確認', '持ち物の一覧'),
 'beauty': ('ケア手順を整理', '製品の説明を確認', '手順の一覧'),
 'cooking': ('今夜の献立を考える', '手元の食材を使う', '材料と手順'),
 'education': ('学習範囲を整理', '教材の範囲に限定', '確認問題3つ'),
 'career': ('職務経験を整理', '事実だけを書き出す', '箇条書きの下書き'),
 'lifestyle': ('家事の手順を整理', '使える時間を確認', '作業の順番'),
 'technology': ('設定手順を整理', '機器の型番を確認', '確認手順の一覧'),
}
COLORS = {'background':'#07192B','panel':'#0B3047','teal':'#44DAD3','white':'#F6FCFF','muted':'#C3DDE8'}

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()

def validate(genre):
 if genre not in GENRES or len(GENRES)!=10: raise ValueError('unsupported genre')
 if SCENE_END-SCENE_START != 87 or SAFE_Y>=1490: raise RuntimeError('unsafe scene or subtitle geometry')
 if 'PUBLICATION_NOT_APPROVED' not in POLICY: raise RuntimeError('publication guard missing')
 if not Path(FONT).exists() or not Path(BOLD).exists(): raise FileNotFoundError('Japanese fonts missing')
 for triple in GENRES.values():
  if len(triple)!=3 or any(len(x)>16 for x in triple): raise ValueError('unsafe prompt length')

def phase(local_frame):
 if not 0<=local_frame<87: raise ValueError('frame outside scene04')
 return min(2,local_frame//29)

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)

def draw_prompt(local_frame,genre='ai_work'):
 validate(genre)
 p=phase(local_frame)
 im=Image.new('RGBA',(WIDTH,SAFE_Y),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rectangle((0,145,WIDTH,1430),fill=(5,20,35,251))
 d.rounded_rectangle((45,185,1035,1405),radius=40,fill=(6,26,43,253),outline=(62,123,143,255),width=3)
 d.text((85,217),'AIへの指示を組み立てる',font=font(54,True),fill=COLORS['white'])
 d.text((88,303),'架空の入力例・実操作映像ではありません',font=font(29),fill=COLORS['muted'])
 d.rounded_rectangle((78,379,1002,1075),radius=26,fill=(13,49,71,255),outline=(56,112,131,255),width=3)
 labels=('目的','条件','出力')
 for i,(label,value) in enumerate(zip(labels,GENRES[genre])):
  y=415+i*216
  active=i==p
  d.rounded_rectangle((101,y,980,y+180),radius=22,
   fill=(14,87,94,255) if active else (18,61,80,255),
   outline=(67,226,217,255) if active else (49,98,117,255),width=5 if active else 2)
  d.rounded_rectangle((120,y+26,251,y+83),radius=14,fill=(60,220,211,255) if active else (39,93,111,255))
  d.text((141,y+26),label,font=font(37,True),fill='#062C38' if active else '#D5E8EF')
  # Phase-aware character reveal: previous steps remain visible, upcoming steps are masked.
  if i<p: visible=value
  elif i==p:
   elapsed=local_frame-p*29
   visible=value[:max(1,min(len(value),int((elapsed+2)*len(value)/23)))]
  else: visible='入力待ち'
  d.text((283,y+24),visible,font=font(44,True) if i<=p else font(37),
   fill=COLORS['white'] if i<=p else '#789BAC')
  if active and (local_frame//6)%2==0:
   bb=d.textbbox((283,y+24),visible,font=font(44,True))
   d.rectangle((min(bb[2]+6,950),y+34,min(bb[2]+10,954),y+84),fill='#D7FFFF')
  if i<p:d.text((842,y+106),'入力済み',font=font(26,True),fill='#86E8DF')
 d.rounded_rectangle((92,1114,988,1205),radius=20,fill=(8,87,97,255))
 d.text((126,1131),'目的 → 条件 → 出力 の順に指定',font=font(39,True),fill=COLORS['white'])
 for i in range(3):
  d.rounded_rectangle((333+i*143,1242,450+i*143,1258),radius=7,fill=COLORS['teal'] if i<=p else '#365A70')
 d.text((151,1322),'※ 内容は元データで確認・社員承認後に手動投稿',font=font(27),fill='#B5D5DC')
 return im

def command(args,log):
 p=subprocess.run(args,capture_output=True,text=True)
 Path(log).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 if p.returncode: raise RuntimeError('command failed: '+p.stderr[-1200:])

def render(source,output,workdir,genre='ai_work',expected_source_sha=None):
 validate(genre);source=Path(source);output=Path(output);workdir=Path(workdir)
 if not source.is_file():raise FileNotFoundError(source)
 digest=sha256(source)
 if expected_source_sha and digest!=expected_source_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 workdir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 od=workdir/'overlays';od.mkdir(exist_ok=True)
 for i in range(87):draw_prompt(i,genre).save(od/f'{i:03d}.png',compress_level=1)
 # Transparent overlay limited to the top 1450px; preserve the subtitle band.
 graph=f"[1:v]setpts=PTS+{SCENE_START}/30/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{SCENE_START},{SCENE_END-1})'[v]"
 command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-framerate','30','-start_number','0','-i',str(od/'%03d.png'),
          '-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264',
          '-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30',
          '-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)],workdir/'encode.log')
 result={'policy':POLICY,'genre':genre,'source_sha256':digest,'output_sha256':sha256(output),
         'changed_frame_range':[SCENE_START,SCENE_END-1],'subtitle_safe_y':SAFE_Y,
         'real_app_recording':False,'original_japanese_narration':'INHERITED_NOT_ASR_VERIFIED',
         'employee_approval':'NOT_APPROVED','public_media_upload':False,
         'assets':'original Pillow graphics and authorized inherited private MP4'}
 (workdir/'render_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--output',required=True)
 a.add_argument('--workdir',required=True);a.add_argument('--genre',choices=GENRES,default='ai_work');a.add_argument('--expected-source-sha')
 z=a.parse_args();print(json.dumps(render(z.source,z.output,z.workdir,z.genre,z.expected_source_sha),ensure_ascii=False))
