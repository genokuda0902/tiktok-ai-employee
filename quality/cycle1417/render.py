"""Review-only, privacy-safe reimplementation. No voice: fail closed."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, json
ROOT=Path(__file__).parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('売上集計、15秒で時短','手計算から関数へ切り替え'),('売上を入力','3,200円 / 4,100円 / 5,100円'),('SUM関数を入力','=SUM(B2:B4)'),('結果を確認','合計 12,400円'),('次に試してみよう','保存してあとで見返す')]
assert len(SCENES)==5
W,H=540,960
font=lambda p,s:ImageFont.truetype(p,s)
def draw_frame(i,t):
 im=Image.new('RGB',(W,H),'#091426'); d=ImageDraw.Draw(im)
 d.rounded_rectangle((22,110,518,770),radius=24,fill='#15263c')
 d.rectangle((22,110,30,770),fill='#20d4cb')
 d.text((32,35),'AI時短ラボ  |  15秒で実演',font=font(BOLD,25),fill='white')
 d.text((40,160),SCENES[i][0],font=font(BOLD,31),fill='#ffffff')
 if i in (1,2,3):
  for row,(name,value) in enumerate([('売上1','3,200'),('売上2','4,100'),('売上3','5,100')]):
   y=270+row*82
   d.rounded_rectangle((50,y,490,y+68),radius=9,fill='#273c53' if i!=1 or row>int(t*3)%3 else '#287d78')
   d.text((68,y+15),name,font=font(FONT,22),fill='white')
   d.text((320,y+15),value,font=font(BOLD,24),fill='white')
  if i==2:
   text=SCENES[i][1][:max(1,int(t*len(SCENES[i][1])/2.4))]
   d.text((55,580),text,font=font(BOLD,29),fill='#54f3d6')
  if i==3:d.text((55,590),'12,400 円',font=font(BOLD,45),fill='#54f3d6')
 else:d.text((45,360),SCENES[i][1],font=font(FONT,22),fill='#d5e7fa')
 d.rounded_rectangle((26,800,514,896),radius=14,fill='#000000')
 d.text((40,825),SCENES[i][1],font=font(FONT,22),fill='white')
 d.rounded_rectangle((26,922,514,932),radius=5,fill='#2b3a50')
 d.rounded_rectangle((26,922,26+int(488*(i+t/3)/5),932),radius=5,fill='#20d4cb')
 return im
def render():
 frames=ROOT/'frames';frames.mkdir(exist_ok=True)
 for k in range(75):
  i=k//15;t=(k%15)/5
  draw_frame(i,t).save(frames/f'{k:04d}.png')
 out=ROOT/'cycle1417_REVIEW_ONLY.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','5','-i',str(frames/'%04d.png'),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-pix_fmt','yuv420p','-r','25','-movflags','+faststart','-an',str(out)],check=True)
 (ROOT/'manifest.json').write_text(json.dumps({'status':'PUBLICATION_NOT_APPROVED','scenes':SCENES,'audio':'UNAVAILABLE','subtitle':'visual scene captions, not synchronized speech','duration_s':15,'assets':'original procedural graphics only'},ensure_ascii=False,indent=2))
 print(out)
if __name__=='__main__':render()
