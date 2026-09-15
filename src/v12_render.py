#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
from pathlib import Path
import subprocess,wave,math,shutil
W,H,FPS=1080,1920,30; O=Path('output');O.mkdir(exist_ok=True)
voice=O/'narration.wav'; op=O/'v9_operation.mp4'; final=O/'AI時短ラボ_01_v12.mp4'
for p in (voice,op):
 if not p.exists(): raise SystemExit(f'missing {p}')
with wave.open(str(voice),'rb') as w: dur=w.getnframes()/w.getframerate()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def F(n):return ImageFont.truetype(font,n)
def text(d,xy,s,n,fill='white',stroke=0,sc='black'):d.text(xy,s,font=F(n),fill=fill,stroke_width=stroke,stroke_fill=sc)
def bg():
 im=Image.new('RGB',(W,H),'#071426');d=ImageDraw.Draw(im)
 for r in range(760,30,-35):
  a=max(0,1-r/800); col=(int(7+10*a),int(20+80*a),int(38+130*a));d.ellipse((540-r,610-r,540+r,610+r),fill=col)
 return im
def robot(im,x=540,y=760,scale=1.0,wink=False):
 d=ImageDraw.Draw(im); s=scale
 # glow
 d.ellipse((x-270*s,y-330*s,x+270*s,y+250*s),fill='#0a3151')
 # body
 d.rounded_rectangle((x-145*s,y+70*s,x+145*s,y+400*s),int(80*s),fill='#eef7ff',outline='#74dfff',width=max(2,int(8*s)))
 d.rounded_rectangle((x-225*s,y-220*s,x+225*s,y+150*s),int(120*s),fill='#f7fbff',outline='#8be8ff',width=max(2,int(9*s)))
 d.rounded_rectangle((x-185*s,y-170*s,x+185*s,y+85*s),int(85*s),fill='#071522')
 d.ellipse((x-105*s,y-80*s,x-45*s,y-20*s),fill='#28e7ff')
 if wink:d.arc((x+45*s,y-65*s,x+115*s,y-10*s),0,180,fill='#28e7ff',width=max(3,int(10*s)))
 else:d.ellipse((x+45*s,y-80*s,x+105*s,y-20*s),fill='#28e7ff')
 d.rounded_rectangle((x-75*s,y+175*s,x+75*s,y+270*s),int(18*s),fill='#102a45');text(d,(x-43*s,y+188*s),'AI',int(48*s),'#42e8ff')
 # arms gesture
 d.line((x-145*s,y+150*s,x-315*s,y+10*s),fill='#eaf6ff',width=max(10,int(55*s)));d.ellipse((x-345*s,y-35*s,x-285*s,y+25*s),fill='#eef7ff')
 d.line((x+145*s,y+150*s,x+315*s,y-15*s),fill='#eaf6ff',width=max(10,int(55*s)));d.ellipse((x+285*s,y-50*s,x+350*s,y+15*s),fill='#eef7ff')
def titlecard(head,sub,accent='#35e7ff',mode='robot'):
 im=bg();d=ImageDraw.Draw(im)
 text(d,(58,92),'AI時短ラボ',50,'white'); d.rectangle((58,158,420,166),fill=accent)
 if mode=='robot':robot(im,540,700,.92,True)
 elif mode=='pain':
  d.rounded_rectangle((90,390,990,1160),55,fill='#17243a',outline='#64748b',width=4)
  for j,s in enumerate(['資料作成に時間がかかる…','データ集計が面倒…','同じ作業の繰り返し…']):
   d.rounded_rectangle((145,480+j*190,935,610+j*190),32,fill='#f8fafc');text(d,(190,510+j*190),s,40,'#111827')
 elif mode=='apps':
  robot(im,540,760,.75,False); d.rounded_rectangle((105,410,470,650),50,fill='#10a37f');text(d,(175,485),'ChatGPT',45);d.rounded_rectangle((610,410,975,650),50,fill='#107c41');text(d,(720,485),'Excel',52)
 text(d,(70,1320),head,72,'white',5,'#020617');text(d,(72,1430),sub,48,accent,3,'#020617')
 return im
scenes=[
 ('これ、まだ\n手でやってる？','ChatGPT×Excelで一瞬','robot'),
 ('こんな悩み\nありませんか？','繰り返し作業をAIへ','pain'),
 ('ChatGPT×Excel','仕事を一気に時短','apps'),
 ('やりたいことを\n自然な言葉で','入力するだけ','apps'),
 ('数秒で分析','表・要点まで自動','apps'),
 ('結果を確認','必要な情報が一覧に','apps'),
 ('Excelへ貼付','コピペで完成','apps'),
 ('グラフも要点も','一気に見える化','apps'),
 ('Before → After','面倒な作業を短縮','pain'),
 ('他にも使える','要約・メール・可視化','robot'),
 ('保存して試す','毎日1つAI仕事術','robot'),
 ('次回予告','営業メールを10秒で','robot'),
 ('AI時短ラボ','AIで自由な時間を','robot'),
 ('時短 × 効率化','仕事をもっとラクに','robot'),
 ('フォローで続き','明日会社で使えるAI','robot'),
 ('また次の動画で','お会いしましょう！','robot')]
weights=[2,2,2,2,2,2,2,2,4,4,4,2,2,2,1,1];s=sum(weights);bounds=[0]
for q in weights:bounds.append(bounds[-1]+dur*q/s)
frames=O/'v12_frames';shutil.rmtree(frames,ignore_errors=True);frames.mkdir()
for n in range(math.ceil(dur*FPS)):
 t=min(n/FPS,dur-1e-4);idx=next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15);u=(t-bounds[idx])/max(.01,bounds[idx+1]-bounds[idx])
 base=titlecard(*scenes[idx]); z=1.0+.035*u; rs=base.resize((int(W*z),int(H*z)),Image.Resampling.LANCZOS);l=(rs.width-W)//2;top=(rs.height-H)//2;base=rs.crop((l,top,l+W,top+H))
 base.save(frames/f'{n:05d}.png',compress_level=1)
scene=O/'v12_brand.mp4';subprocess.run(['ffmpeg','-y','-framerate','30','-i',str(frames/'%05d.png'),'-c:v','libx264','-preset','slow','-crf','13','-pix_fmt','yuv420p','-t',f'{dur:.3f}',str(scene)],check=True)
# Put operation proof inside the same branded shell, not as a full-screen foreign-looking cutaway.
start=bounds[3];end=bounds[8];pd=end-start
fc=(f"[1:v]scale=900:1600:flags=lanczos,trim=0:{pd:.3f},setpts=PTS-STARTPTS+{start:.3f}/TB[proof];"
    f"[0:v][proof]overlay=90:205:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass[v]")
subprocess.run(['ffmpeg','-y','-i',str(scene),'-i',str(op),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{dur:.3f}','-c:v','libx264','-preset','slow','-crf','13','-maxrate','14M','-bufsize','28M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)],check=True)
print(final)
