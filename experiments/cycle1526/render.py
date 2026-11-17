"""Review-only synthetic spreadsheet demo. No real data or narration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'cycle1526_REVIEW_ONLY.mp4'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('入力ミス、減らせる？','毎回、合計を手計算していませんか？'),('範囲を選択','B2 から B5 を選びます'),('SUMを入力','=SUM(B2:B5)'),('結果を照合','合計 12,800 円を確認')]
FPS=24; DURATION=12; W=720; H=1280
f=ImageFont.truetype(FONT,32); big=ImageFont.truetype(BOLD,53); small=ImageFont.truetype(FONT,23)
def scene_at(t): return min(int(t//3),len(SCENES)-1)
def render():
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-t',str(DURATION),'-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for k in range(FPS*DURATION):
  t=k/FPS; idx=scene_at(t); title,caption=SCENES[idx]
  im=Image.new('RGB',(W,H),'#0b1426'); d=ImageDraw.Draw(im)
  d.rounded_rectangle((34,85,686,1150),radius=28,fill='#17283d')
  d.text((60,122),'AI時短ラボ  /  REVIEW ONLY',font=small,fill='#8fe5d7')
  d.text((60,235),title,font=big,fill='white')
  d.rounded_rectangle((57,352,663,908),radius=16,fill='#f3f7fc')
  d.rectangle((57,352,663,411),fill='#197a69');d.text((82,361),'架空データの売上表',font=f,fill='white')
  for row,val in enumerate((1200,2800,3900,4900)):
   y=440+row*92
   if idx>=1 and row<4: d.rounded_rectangle((407,y-3,626,y+58),radius=6,fill='#d5f4ea')
   d.text((85,y),f'商品 {row+1}',font=f,fill='#273747')
   d.text((444,y),f'{val:,}',font=f,fill='#273747')
   d.line((79,y+66,638,y+66),fill='#d1dce8',width=2)
  if idx>=2:
   d.rounded_rectangle((82,831,634,901),radius=8,fill='#d4f3e9');d.text((104,842),'=SUM(B2:B5)',font=f,fill='#12634d')
  if idx>=3:
   d.rounded_rectangle((75,936,643,1016),radius=12,fill='#1b7968');d.text((103,947),'合計 12,800 円',font=f,fill='white')
  d.rounded_rectangle((40,1034,680,1110),radius=14,fill='#07101c')
  d.text((58,1050),caption,font=small,fill='#ffffff')
  d.rounded_rectangle((56,1130,664,1139),radius=4,fill='#30435b')
  d.rounded_rectangle((56,1130,56+int(608*t/DURATION),1139),radius=4,fill='#63dfc5')
  d.text((55,1190),'日本語音声なし / 発話同期字幕なし / 投稿禁止',font=small,fill='#ffb5a7')
  p.stdin.write(im.tobytes())
 p.stdin.close(); assert p.wait()==0
 return OUT
if __name__=='__main__': print(render())
