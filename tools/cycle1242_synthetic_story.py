"""Synthetic-only story renderer; no private assets. Requires Pillow and FFmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, sys
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path("review.mp4")
tmp=out.parent/"frames"; tmp.mkdir(parents=True,exist_ok=True)
font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
bold="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def f(n,b=False): return ImageFont.truetype(bold if b else font,n)
scenes=[("BEFORE","手作業で合計を計算","120 + 180 = ?","毎回、電卓で確認"),("ACTION","SUM関数を入力","=SUM(B2:B3)","セルに数式を入力"),("AFTER","合計が自動で表示","300","数値が変わっても再計算")]
for i,(stage,headline,formula,sub) in enumerate(scenes):
 im=Image.new("RGB",(720,1280),"#0b1424"); d=ImageDraw.Draw(im)
 d.rounded_rectangle((35,90,685,1150),radius=35,fill="#17263d")
 d.text((62,130),f"{i+1:02d} / 03   {stage}",font=f(30,True),fill="#5fe0d1")
 d.text((62,235),headline,font=f(40,True),fill="white")
 d.rounded_rectangle((62,345,658,855),radius=16,fill="#f5f7fa")
 for y in [415,510,605,700,795]: d.line((82,y,635,y),fill="#c6d2de",width=2)
 for x in [155,400,630]: d.line((x,370,x,820),fill="#c6d2de",width=2)
 for y,t in [(380,"項目"),(465,"売上A"),(560,"売上B"),(655,"合計")]: d.text((95,y),t,font=f(25),fill="#18263a")
 for y,t in [(465,"120"),(560,"180")]: d.text((455,y),t,font=f(32),fill="#18263a")
 d.rounded_rectangle((415,640,618,700),radius=8,fill="#b7f3e9" if i==2 else "#e4eaf1")
 d.text((432,648),"300" if i==2 else ("SUM" if i==1 else "???"),font=f(29,True),fill="#132536")
 d.text((65,900),formula,font=f(45,True),fill="#5fe0d1")
 d.text((65,1010),sub,font=f(29),fill="white")
 d.rounded_rectangle((62,1190,658,1204),radius=7,fill="#35455b")
 d.rounded_rectangle((62,1190,62+(i+1)*198,1204),radius=7,fill="#5fe0d1")
 im.save(tmp/f"{i}.png")
cmd=["ffmpeg","-y"]
for i in range(3): cmd+=["-loop","1","-framerate","30","-t","5","-i",str(tmp/f"{i}.png")]
cmd+=["-filter_complex","[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]","-map","[v]","-c:v","libx264","-preset","ultrafast","-crf","25","-movflags","+faststart",str(out)]
subprocess.run(cmd,check=True)
