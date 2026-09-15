#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,wave,math,shutil
W,H,FPS=1080,1920,30;O=Path('output');O.mkdir(exist_ok=True)
voice=O/'narration.wav';proof=O/'v9_operation.mp4';final=O/'AI時短ラボ_01_v13.mp4'
with wave.open(str(voice),'rb') as w:DUR=w.getnframes()/w.getframerate()
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def F(n):return ImageFont.truetype(FONT,n)
def T(d,x,y,s,n,c='white',sw=4):d.text((x,y),s,font=F(n),fill=c,stroke_width=sw,stroke_fill='#020617')
def bg(seed):
 im=Image.new('RGB',(W,H),'#050e1d');d=ImageDraw.Draw(im)
 for i in range(22):
  x=(seed*127+i*173)%W;y=(seed*211+i*307)%H;r=70+(i%5)*45;d.ellipse((x-r,y-r,x+r,y+r),fill=(4,24+(i%3)*11,48+(i%4)*14))
 d.rectangle((0,0,W,190),fill='#050d19');T(d,55,48,'AI時短ラボ',50);d.rectangle((55,132,390,141),fill='#28e8ff');return im
def bot(im,x=540,y=680,s=1,wink=False,pose=0):
 d=ImageDraw.Draw(im);d.ellipse((x-300*s,y-310*s,x+300*s,y+330*s),fill='#093854');d.rounded_rectangle((x-215*s,y-180*s,x+215*s,y+175*s),int(115*s),fill='#f5fbff',outline='#4ce5ff',width=max(3,int(10*s)));d.rounded_rectangle((x-174*s,y-130*s,x+174*s,y+78*s),int(70*s),fill='#06131f');d.ellipse((x-100*s,y-58*s,x-40*s,y+2*s),fill='#28eaff')
 if wink:d.arc((x+35*s,y-45*s,x+108*s,y+8*s),0,180,fill='#28eaff',width=max(3,int(11*s)))
 else:d.ellipse((x+40*s,y-58*s,x+100*s,y+2*s),fill='#28eaff')
 d.rounded_rectangle((x-135*s,y+135*s,x+135*s,y+430*s),int(65*s),fill='#eef9ff',outline='#4ce5ff',width=max(3,int(8*s)));d.rounded_rectangle((x-65*s,y+225*s,x+65*s,y+305*s),16,fill='#092943');T(d,x-36*s,y+229*s,'AI',int(40*s),'#31eaff',1)
 if pose%2==0:d.line((x+135*s,y+205*s,x+345*s,y+20*s),fill='#eef9ff',width=max(18,int(58*s)))
 else:d.line((x-135*s,y+205*s,x-330*s,y+20*s),fill='#eef9ff',width=max(18,int(58*s)))
def make(kind,h1,h2,seed):
 im=bg(seed);d=ImageDraw.Draw(im)
 if kind=='hero':bot(im,540,650,1.12,seed%2==0,seed);T(d,65,1240,h1,80);T(d,65,1450,h2,52,'#32e9ff')
 elif kind=='pain':
  d.rounded_rectangle((60,315,1020,1225),55,fill='#eef2f7');T(d,120,370,'仕事あるある',54,'#111827',1)
  for j,s in enumerate(['資料作成が終わらない','データ集計が面倒','同じ作業の繰り返し']):d.rounded_rectangle((115,520+j*205,965,665+j*205),32,fill='white',outline='#cbd5e1',width=3);T(d,160,558+j*205,s,40,'#111827',1)
  T(d,65,1350,h1,70);T(d,65,1510,h2,48,'#ffd21f')
 elif kind=='apps':
  d.rounded_rectangle((75,360,1005,1190),55,fill='#0a2138',outline='#27e5ff',width=5);T(d,130,450,'ChatGPT',62,'#5cf0c7');T(d,430,560,'×',80);T(d,590,450,'Excel',66,'#67e494');bot(im,750,900,.62,seed%2==0,seed);T(d,65,1320,h1,70);T(d,65,1490,h2,48,'#32e9ff')
 elif kind=='ba':
  d.rounded_rectangle((55,310,510,1230),42,fill='#252a34');d.rounded_rectangle((570,310,1025,1230),42,fill='#073e70');T(d,145,365,'BEFORE',46,'#ffd21f');T(d,685,365,'AFTER',46,'#32e9ff');T(d,105,610,'手入力',62);T(d,105,760,'集計',62);T(d,105,910,'グラフ',62);T(d,640,640,'AIで',72);T(d,615,790,'一気に',72);T(d,625,940,'完成',72,'#ffd21f');T(d,65,1350,h1,66);T(d,65,1510,h2,46,'#32e9ff')
 elif kind=='cta':bot(im,540,650,1.08,True,seed);T(d,65,1260,h1,70);d.rounded_rectangle((120,1480,960,1650),55,fill='#ff315f');T(d,285,1515,h2,54)
 return im
beats=[('hero','その作業、まだ\n手でやってる？','ChatGPT×Excel'),('pain','毎日のコピペ','時間取られてませんか？'),('apps','ChatGPT×Excel','ここまで変わる'),('apps','日本語で指示','やりたいことを書く'),('apps','AIが分析','項目を自動整理'),('apps','表に変換','そのまま使える'),('apps','Excelへ','貼り付け'),('apps','数字から','グラフまで'),('ba','手入力 → AI','面倒な作業を短縮'),('apps','要約・メール','資料作成にも'),('hero','仕事の幅が','一気に広がる'),('hero','営業・事務にも','すぐ使える'),('hero','AIで働き方を','もっと自由に'),('cta','役に立ったら','フォローする'),('hero','次回は営業メール','10秒で作る'),('cta','明日会社で使えるAI','フォローする')]
# 16 beats mapped to narration duration; first 8 are deliberately fast, later beats remain varied.
wts=[1.25,1.35,1.2,1.0,1.0,1.0,1.0,1.0,1.55,1.35,1.25,1.25,1.3,1.25,1.2,1.25];S=sum(wts);B=[0]
for q in wts:B.append(B[-1]+DUR*q/S)
frames=O/'v13_frames';shutil.rmtree(frames,ignore_errors=True);frames.mkdir()
for n in range(math.ceil(DUR*FPS)):
 t=min(n/FPS,DUR-.001);i=next((k for k in range(16) if B[k]<=t<B[k+1]),15);u=(t-B[i])/max(.01,B[i+1]-B[i]);im=make(*beats[i],i)
 # TikTok camera language: push, slight horizontal drift, alternating framing
 z=1.02+.055*u;rw,rh=int(W*z),int(H*z);im=im.resize((rw,rh),Image.Resampling.LANCZOS);dx=int((rw-W)*(u if i%2 else 1-u));dy=(rh-H)//2;im=im.crop((dx,dy,dx+W,dy+H))
 # progress accent / kinetic top marker
 d=ImageDraw.Draw(im);d.rectangle((0,184,int(W*(t/DUR)),192),fill='#2ce8ff');im.save(frames/f'{n:05d}.jpg',quality=95,subsampling=0)
brand=O/'v13_brand.mp4';subprocess.run(['ffmpeg','-y','-framerate','30','-i',str(frames/'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-t',f'{DUR:.3f}',str(brand)],check=True)
# Proof becomes the hero during beats 4-8, but is framed by brand chrome and followed by native before/after.
start=B[3];end=B[8];pd=end-start
fc=f"[1:v]scale=960:1706:force_original_aspect_ratio=decrease,pad=960:1706:(ow-iw)/2:(oh-ih)/2:#06101e,trim=0:{pd:.3f},setpts=PTS-STARTPTS+{start:.3f}/TB[p];[0:v][p]overlay=60:195:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass[v]"
subprocess.run(['ffmpeg','-y','-i',str(brand),'-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{DUR:.3f}','-c:v','libx264','-preset','slow','-crf','14','-maxrate','14M','-bufsize','28M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)],check=True)
subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=codec_name,width,height','-of','default=nw=1',str(final)],check=True)
print(final)
