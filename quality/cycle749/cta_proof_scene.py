#!/usr/bin/env python3
"""Image-first proof CTA for 10 genres; offline, synthetic data only.

Never use unapproved source media or present this as AI-operating-Calc footage.
Original reference v33 is NOT reproduced by this reimplementation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=540,960,30
START=729  # 24.3 s, after previous Calc proof scene
END=819    # 27.3 s; inherited narration continues to 27.343
ACCENTS={
 'ai_work':(46,229,221),'romance':(255,148,182),'beauty':(240,182,221),
 'money':(160,220,131),'trivia':(245,197,111),'gadgets':(116,186,253),
 'health':(116,222,175),'sales':(255,167,102),'travel':(117,205,241),
 'mystery':(183,154,255)}
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def f(n,b=True):return ImageFont.truetype(BOLD if b else REG,n)
def smooth(t):
 t=max(0.,min(1.,float(t)))
 return t*t*(3-2*t)

def verify_contract(values=(120000,150000,200000,180000),formula='=SUM(B2:B5)'):
 if len(values)!=4 or any(type(v) is not int or v<0 for v in values):
  raise ValueError('four nonnegative integer amounts required')
 if formula!='=SUM(B2:B5)':raise ValueError('formula must match B2:B5 proof')
 return sum(values)

def capture_crop(path):
 """Real locally captured Calc screenshot, only allowed synthetic CSV source."""
 p=Path(path)
 if p.name!='calc_b6.png' or not p.is_file():raise ValueError('only local synthetic calc_b6.png allowed')
 im=Image.open(p).convert('RGB')
 if im.size!=(1600,1000):raise ValueError('unexpected capture dimensions')
 # Hide desktop and application chrome; preserve the actual formula bar and cells.
 clean=Image.new('RGB',(455,212),'white')
 clean.paste(im.crop((55,147,510,189)),(0,0))
 clean.paste(im.crop((55,263,510,433)),(0,42))
 return clean.resize((468,184),Image.Resampling.LANCZOS)

def draw_frame(frame:int,capture:Image.Image,genre='ai_work'):
 if not 0<=frame<END-START:raise ValueError('frame outside CTA')
 if genre not in ACCENTS:raise ValueError('unsupported genre')
 if capture.size!=(468,184):raise ValueError('capture must be 468x184')
 accent=ACCENTS[genre]; t=frame/(END-START-1)
 im=Image.new('RGB',(W,H),(5,15,31));d=ImageDraw.Draw(im)
 for y in range(H):
  d.line((0,y,W,y),fill=(5+int(y/H*8),16+int(y/H*10),31+int(y/H*19)))
 glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow)
 g.ellipse((-190,-90,500,580),fill=(*accent,58))
 g.ellipse((220,420,750,1010),fill=(64,91,235,52))
 im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(76)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((25,65,515,109),radius=12,fill=(11,45,60),outline=accent,width=2)
 d.text((42,75),'AI時短ラボ  /  保存して試す',font=f(20),fill='white')
 d.text((27,140),'見るだけで終わらせない。',font=f(31),fill='white')
 d.text((27,188),'次の3ステップ',font=f(42),fill=accent)
 # Stage-specific progression that preserves an unambiguous, static CTA.
 stages=['架空データを用意','B6に数式を入力','65万円を確認']
 for i,lab in enumerate(stages):
  y=266+i*67;active=t>=(i*.28)
  d.rounded_rectangle((25,y,515,y+54),radius=12,
                      fill=(15,58,71) if active else (12,34,52),
                      outline=accent if active else (66,93,113),width=2 if active else 1)
  d.rounded_rectangle((39,y+9,76,y+45),radius=9,fill=accent if active else (37,64,80))
  d.text((50,y+11),str(i+1),font=f(22),fill=(2,23,34) if active else (213,233,242))
  d.text((92,y+10),lab,font=f(24),fill='white' if active else (162,188,202))
 # A verified Calc screenshot, no recreated UI values.
 d.rounded_rectangle((23,489,517,738),radius=19,fill=(5,24,42),outline=accent,width=2)
 d.text((39,505),'実際のCalc画面 / 架空データ',font=f(18),fill=(213,240,242))
 im.paste(capture,(36,547));d=ImageDraw.Draw(im)
 d.rounded_rectangle((29,766,511,850),radius=17,fill=(8,36,52),outline=accent,width=2)
 d.text((43,780),'=SUM(B2:B5)',font=f(30),fill=accent)
 d.text((307,789),'→ 650,000円',font=f(20),fill='white')
 # The CTA's spoken caption; no fake voice or fake AI action.
 d.text((32,868),'保存して、あとで試してみて。',font=f(22),fill='white')
 d.text((32,910),'※ 操作再構成・架空データ／公開未承認',font=f(14,False),fill=(173,203,213))
 # Animate a modest line only, avoiding zoom that would crop readable evidence.
 d.rounded_rectangle((28,948,28+round(484*smooth(t)),952),radius=2,fill=accent)
 return im.convert('RGB')

def render_scene(capture,output,genre='ai_work'):
 screenshot=capture_crop(capture)
 out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
      '-s','540x960','-r','30','-i','-','-vf','scale=1080:1920:flags=lanczos',
      '-an','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(out)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for frame in range(END-START):p.stdin.write(draw_frame(frame,screenshot,genre).tobytes())
 finally:p.stdin.close()
 if p.wait()!=0:raise RuntimeError('scene render failed')

def assemble(source,scene,output):
 start=START/FPS;end=(END-1)/FPS
 filt=(f'[1:v]setpts=PTS-STARTPTS+{start:.6f}/TB[insert];'
       f'[0:v][insert]overlay=0:0:eof_action=pass:enable=between(t\\,{start:.6f}\\,{end:.6f}),format=yuv420p[v]')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(scene),
  '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
  '-crf','20','-r','30','-c:a','copy','-movflags','+faststart',str(output)],check=True)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--capture',type=Path,required=True)
 p.add_argument('--source',type=Path,required=True)
 p.add_argument('--scene',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--genre',choices=ACCENTS,default='ai_work')
 a=p.parse_args();verify_contract();render_scene(a.capture,a.scene,a.genre)
 assemble(a.source,a.scene,a.output)
