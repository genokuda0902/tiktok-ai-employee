#!/usr/bin/env python3
"""Offline speech-pause subtitle reveals. Review only; NOT speech recognition."""
import argparse, json, re, subprocess
from pathlib import Path

GENRES=('ai_work','business','money','learning','health','lifestyle','psychology','science','history','travel')
SCENES=[
 (0,3.133333,'AIで仕事を速くするなら、','最初の一歩が大事。'),
 (3.133333,5.6,'まず、繰り返している','作業を書き出す。'),
 (5.6,8.233333,'次に、完成形の見本を','用意する。'),
 (8.233333,11.,'指示は、目的と条件を','具体的に伝える。'),
 (11.,13.733333,'最初の出力は、','必ず自分で確かめる。'),
 (13.733333,16.633333,'違いがあれば、修正点を','一つずつ伝える。'),
 (16.633333,19.166667,'使える指示は、','テンプレートに残す。'),
 (19.166667,22.5,'小さな時短を、','毎日の習慣にしよう。')]
def find_pauses(path,noise_db=-38,min_duration=0.16):
 cmd=['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn',
      '-af',f'silencedetect=noise={noise_db}dB:d={min_duration}','-f','null','-']
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1200:])
 starts=[];gaps=[]
 for line in p.stderr.splitlines():
  a=re.search(r'silence_start:\s*([\d.]+)',line)
  if a:starts.append(float(a.group(1)))
  b=re.search(r'silence_end:\s*([\d.]+)',line)
  if b and starts:
   st=starts.pop(0);en=float(b.group(1))
   if en>st:gaps.append((st,en))
 return gaps
def select_reveals(scenes,pauses):
 reveals=[]
 for n,(st,en,first,second) in enumerate(scenes):
  if not first or not second or en<=st:raise ValueError('Invalid scene')
  d=en-st
  candidates=[(a,b) for a,b in pauses if a>=st+.1*d and b<=en-.06*d and b-a>=.18]
  if not candidates:raise ValueError(f'No clear internal speech pause in scene {n+1}')
  a,b=min(candidates,key=lambda g:(abs(((g[0]+g[1])/2-st)/d-.40),-(g[1]-g[0])))
  reveals.append(round(b,3))
 return reveals
def ass_time(t):
 cs=round(t*100);h,r=divmod(cs,360000);m,r=divmod(r,6000);s,cs=divmod(r,100)
 return f'{h}:{m:02}:{s:02}.{cs:02}'
def clean(s):return str(s).replace('\\','').replace('{','（').replace('}','）').replace('\n',' ')
def make_ass(path,scenes,reveals,genre='ai_work'):
 if genre not in GENRES:raise ValueError('Unknown genre')
 if len(scenes)!=len(reveals):raise ValueError('Reveal count mismatch')
 header='''[Script Info]
Title: Speech-pause Japanese captions - HUMAN REVIEW
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,70,200,0,1
Style: Eyebrow,Noto Sans CJK JP,29,&H00E7D4B5,&H00E7D4B5,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,70,200,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 out=[header]
 for i,((st,en,one,two),reveal) in enumerate(zip(scenes,reveals)):
  if not st+.15<reveal<en-.1:raise ValueError(f'Bad reveal {i}')
  s,e,r=ass_time(st),ass_time(en),ass_time(reveal)
  out.append(f'Dialogue: 0,{s},{e},Eyebrow,,0,0,0,,{{\\pos(75,1400)}}音声の要点　{i+1:02} / {len(scenes):02}\n')
  out.append(f'Dialogue: 1,{s},{e},Caption,,0,0,0,,{{\\pos(75,1461)}}{clean(one)}\n')
  out.append(f'Dialogue: 2,{r},{e},Caption,,0,0,0,,{{\\pos(75,1533)\\c&H00D5E04E&\\fad(130,0)}}{clean(two)}\n')
 Path(path).write_text(''.join(out),encoding='utf-8')
def render(src,dst,genre='ai_work',scenes=SCENES,preset='veryfast',reveals=None):
 src,dst=Path(src),Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
 if reveals is None:reveals=select_reveals(scenes,find_pauses(src))
 ass=dst.with_suffix('.ass');make_ass(ass,scenes,reveals,genre)
 assarg=str(ass.resolve()).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
 vf=("drawbox=x=25:y=1370:w=1040:h=286:color=0x031021@1:t=fill,"
     "drawbox=x=42:y=1378:w=860:h=253:color=0x5ae6db@0.85:t=3,"
     "drawbox=x=42:y=1378:w=8:h=253:color=0x5ae6db@1:t=fill,"
     f"ass=filename='{assarg}'")
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-vf',vf,
      '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
      '-c:v','libx264','-preset',preset,'-crf','20','-pix_fmt','yuv420p',
      '-c:a','copy','-movflags','+faststart',str(dst)]
 subprocess.run(cmd,check=True)
 return {'reveals':reveals,'pauses':find_pauses(src),'ass':str(ass)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('input_mp4');p.add_argument('output_mp4')
 p.add_argument('--genre',choices=GENRES,default='ai_work');a=p.parse_args()
 print(json.dumps(render(a.input_mp4,a.output_mp4,a.genre),ensure_ascii=False))
