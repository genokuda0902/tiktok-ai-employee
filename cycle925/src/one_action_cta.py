#!/usr/bin/env python3
"""Cycle925: native-resolution one-action editorial CTA, review-only.

Uses inherited local media; no network, external assets, auto-post or public upload.
Keeps y>=1460 untouched at source-frame level, including burned captions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

POLICY = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
WIDTH, HEIGHT, FPS = 1080, 1920, 30
SAFE_CAPTION_Y = 1460
SCENE_START, SCENE_END = 609, 691
SCENE_FRAMES = SCENE_END - SCENE_START
FONT_REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
 'ai_work': {'accent':'#36E0C4','topic':'週次報告の下書き'},
 'finance': {'accent':'#73D8FF','topic':'支出の分類'},
 'health': {'accent':'#8BE0A2','topic':'生活習慣の記録'},
 'travel': {'accent':'#90B8FF','topic':'旅行の持ち物整理'},
 'beauty': {'accent':'#F0ACD9','topic':'朝のケア記録'},
 'cooking': {'accent':'#FFBF87','topic':'献立の下書き'},
 'education': {'accent':'#D7C0FF','topic':'復習メモの整理'},
 'career': {'accent':'#FFDB91','topic':'面談メモの整理'},
 'lifestyle': {'accent':'#F0B8C6','topic':'家事の段取り'},
 'technology': {'accent':'#9CE8ED','topic':'作業手順の整理'},
}
ACTION_STEPS = ('作業を1つ選ぶ', 'AIで下書きを作る', '人が内容を確認')
CARD_RECT = (72, 348, 1008, 1396)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def validate_geometry():
 assert len(GENRES)==10
 assert all(v['topic'] and v['accent'].startswith('#') and len(v['accent'])==7 for v in GENRES.values())
 assert CARD_RECT[3] < SAFE_CAPTION_Y
 assert SCENE_FRAMES == 82
 assert len(ACTION_STEPS)==3
 return True

def blend_hex(a,b,t):
 def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
 x,y=rgb(a),rgb(b)
 return tuple(round(u*(1-t)+v*t) for u,v in zip(x,y))

def smoothstep(x):
 x=max(0.0,min(1.0,x));return x*x*(3-2*x)

def stage_for_frame(local_frame):
 if local_frame<19:return 0
 if local_frame<45:return 1
 return 2

def make_overlay(local_frame, genre='ai_work'):
 """Return an RGBA overlay with alpha=0 outside protected editorial card."""
 from PIL import Image, ImageDraw, ImageFont, ImageFilter
 if genre not in GENRES:raise ValueError('unknown genre')
 if not (0<=local_frame<SCENE_FRAMES):raise ValueError('frame outside scene')
 config=GENRES[genre]
 accent=config['accent'];accent_rgb=tuple(int(accent[i:i+2],16) for i in (1,3,5))
 im=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0))
 shadow=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0));sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((80,358,1000,1404),radius=52,fill=(0,0,0,135))
 shadow=shadow.filter(ImageFilter.GaussianBlur(17));im.alpha_composite(shadow)
 dr=ImageDraw.Draw(im)
 dr.rounded_rectangle(CARD_RECT,radius=48,fill='#0B2133',outline='#36556A',width=2)
 stage=stage_for_frame(local_frame)
 for k in range(3):
  x=686+k*92
  dr.rounded_rectangle((x,435,x+72,445),radius=5,fill=accent if k<=stage else '#36556A')
 regular=lambda s:ImageFont.truetype(FONT_REGULAR,s)
 bold=lambda s:ImageFont.truetype(FONT_BOLD,s)
 dr.rounded_rectangle((115,414,415,466),radius=24,fill='#183C4B')
 dr.text((140,419),'TODAY  /  ONE ACTION',font=bold(26),fill=accent)
 dr.text((114,495),'今日、1つだけ。',font=bold(73),fill='#FFFFFF',stroke_width=0)
 dr.text((116,602),'まずは、この作業から始める',font=regular(37),fill='#C9DCE7')
 dr.rounded_rectangle((112,690,967,1159),radius=35,fill='#F7FAFC')
 dr.rounded_rectangle((142,724,290,782),radius=19,fill=accent)
 dr.text((165,734),'EXAMPLE',font=bold(27),fill='#0B2133')
 dr.text((150,816),config['topic'],font=bold(63),fill='#102B40')
 dr.line((151,928,922,928),fill='#D8E3E9',width=3)
 active=stage_for_frame(local_frame)
 y=950
 for i,label in enumerate(ACTION_STEPS):
  x=151+i*256
  bg=accent if i==active else '#E4EBF0'
  fg='#0B2133' if i==active else '#526C7C'
  dr.rounded_rectangle((x,y,x+241,y+158),radius=18,fill=bg)
  dr.text((x+13,y+9),f'{i+1:02d}',font=bold(27),fill=fg)
  parts=[('作業を1つ','選ぶ'),('AIで下書き','作る'),('内容を人が','確認')][i]
  dr.text((x+13,y+51),parts[0],font=regular(27),fill=fg)
  dr.text((x+13,y+92),parts[1],font=bold(40),fill=fg)
 dr.rounded_rectangle((112,1194,967,1339),radius=27,fill='#123A4C')
 dr.ellipse((143,1236,200,1293),fill=accent)
 dr.text((161,1244),'✓',font=bold(31),fill='#082637')
 dr.text((222,1225),'確認してから、保存する。',font=bold(43),fill='#FFFFFF')
 dr.text((116,1360),'DEMO  /  HUMAN REVIEW ONLY',font=regular(23),fill='#9AB7C4')
 return im

def render(source, output, genre='ai_work', expected_sha=None):
 import cv2, numpy as np, subprocess
 validate_geometry()
 source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 if expected_sha and sha256(source)!=expected_sha:raise RuntimeError('SOURCE_SHA_MISMATCH')
 cap=cv2.VideoCapture(str(source))
 if not cap.isOpened():raise RuntimeError('SOURCE_OPEN_FAILED')
 if int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))!=WIDTH or int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))!=HEIGHT:raise RuntimeError('BAD_SOURCE_DIMENSIONS')
 fps=cap.get(cv2.CAP_PROP_FPS)
 if abs(fps-FPS)>0.01:raise RuntimeError('BAD_SOURCE_FPS')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 idx=0
 try:
  while True:
   ok,frame=cap.read()
   if not ok:break
   if SCENE_START<=idx<SCENE_END:
    from PIL import Image
    base=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).convert('RGBA')
    overlay=make_overlay(idx-SCENE_START,genre)
    base.alpha_composite(overlay)
    frame=cv2.cvtColor(np.asarray(base.convert('RGB')),cv2.COLOR_RGB2BGR)
   proc.stdin.write(frame.tobytes())
   idx+=1
  proc.stdin.close()
  err=proc.stderr.read().decode(errors='replace')
  rc=proc.wait()
  if rc!=0:raise RuntimeError('ENCODE_FAILED: '+err[-1000:])
 finally:
  cap.release()
  if proc.poll() is None:proc.kill()
 if idx!=691:raise RuntimeError(f'FRAME_COUNT_MISMATCH: {idx}')
 return {'source_sha256':sha256(source),'output_sha256':sha256(output),'frames':idx,'changed_scene_frames':SCENE_FRAMES,'policy':POLICY,'genre':genre}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--genre',default='ai_work',choices=list(GENRES));ap.add_argument('--expected-source-sha');ap.add_argument('--report');args=ap.parse_args()
 result=render(args.source,args.output,args.genre,args.expected_source_sha)
 if args.report:Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
