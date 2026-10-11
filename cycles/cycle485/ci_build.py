"""Reproducible no-cost CI slideshow. Original vector graphics, fictional numbers."""
from pathlib import Path
import subprocess, json, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"; OUT.mkdir(exist_ok=True)
W,H=1080,1920
TEXTS=[
("その数字、","見ただけで終わり？","数字を見ただけで、仕事は変わらない。"),
("目標３件。","実績２件。","たとえば、目標３件に対して実績２件。"),
("差は、","マイナス１件。","差は１件。ここまでは、ただの集計。"),
("原因を、","ひとつ仮説に。","次に、原因の仮説をひとつ書く。"),
("明日の行動を、","ひとつ決める。","そして、明日の行動をひとつ決める。"),
("数字は、","行動に変えよう。","数字を見るだけで終わらせない。")]
TAGS=["HOOK","EXAMPLE","GAP","WHY","ACTION","SAVE"]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def t(d,xy,s,n=42,c="#F4F8F6",b=False):d.text(xy,s,font=f(n,b),fill=c)
def box(d,xy,c="#12263D",r=26,outline="#31516D"):d.rounded_rectangle(xy,radius=r,fill=c,outline=outline,width=3)
def render(i,p):
 im=Image.new("RGB",(W,H),"#081421");d=ImageDraw.Draw(im)
 for y in range(0,H,10):
  shade=int(14+y/H*14);d.rectangle((0,y,W,y+10),fill=(7,shade,30+int(y/H*18)))
 box(d,(65,75,1015,145));t(d,(100,91),"AI WORKFLOW / KPI",27,b=True);t(d,(900,91),f"{i+1:02d}/06",28,"#C7FF67",True)
 for j in range(6):box(d,(75+j*158,171,208+j*158,182),"#C7FF67" if j<=i else "#31465C",4)
 t(d,(78,246),TAGS[i],32,"#74DFF4",True)
 t(d,(78,338),TEXTS[i][0],80,b=True);t(d,(78,445),TEXTS[i][1],80,b=True)
 box(d,(75,645,1005,1445))
 if i==0:
  t(d,(140,721),"DAILY KPI",45,"#74DFF4",True)
  for k,(a,b) in enumerate([("架電数","120"),("アポ","02"),("達成率","67%")]):
   y=850+k*175;box(d,(120,y,960,y+140),"#1D3850")
   t(d,(160,y+35),a,42);t(d,(730,y+18),b if p>k else "—",78,"#C7FF67",True)
 elif i==1:
  for k,(a,n) in enumerate([("目標",3),("実績",2)]):
   y=795+k*270;t(d,(135,y),a,48,b=True)
   box(d,(340,y,340+min(590,int(n/3*590))*(p>=k+1),y+88),"#74DFF4" if k==0 else "#C7FF67",18)
   t(d,(790,y+100),str(n)+" 件",52,b=True)
  t(d,(145,1320),"※架空の説明用データ",29,"#9FB2C4")
 elif i==2:
  t(d,(260,795),"−1",260,"#FF9777",True);t(d,(550,1120),"件",96,b=True)
  if p>=2:t(d,(260,1320),"集計 ≠ 改善",52,"#C7FF67",True)
 elif i==3:
  for k,(a,b) in enumerate([("現象","アポが目標に届かない"),("仮説","質問が浅いのかも"),("確認","通話内容を３件聞く")]):
   y=760+k*210;box(d,(120,y,950,y+174),"#1B344B" if p>k else "#12263D")
   t(d,(155,y+15),a,31,"#C7FF67");t(d,(155,y+78),b if p>k else "…",45,b=True)
 elif i==4:
  for k,(a,b) in enumerate([("行動","冒頭の質問を１つ変える"),("確認する数字","翌日のアポ率")]):
   y=830+k*265;box(d,(120,y,950,y+204),"#1B344B")
   t(d,(154,y+28),a,36,"#74DFF4",True)
   if p>k:t(d,(154,y+98),b,44,b=True)
  if p>=3:t(d,(230,1350),"仮説 → 行動 → 検証",42,"#C7FF67",True)
 else:
  for k,(a,c) in enumerate([("SEE","#9FB2C4"),("THINK","#74DFF4"),("DO","#C7FF67")]):
   if p>=k:t(d,(340,770+k*200),a,112,c,True)
 box(d,(75,1535,1005,1735),"#172C45")
 t(d,(115,1565),"VOICE SCRIPT / SUBTITLE",28,"#74DFF4",True)
 t(d,(115,1635),TEXTS[i][2],34,b=True)
 t(d,(78,1790),"架空の説明用データ／投稿未承認",25,"#A4B6C8")
 return im
def main():
 paths=[]
 for i in range(6):
  for p in range(4):
   name=OUT/f"frame_{i:02d}_{p}.png";render(i,p).save(name);paths.append(name)
 concat=OUT/"concat.txt"
 with concat.open("w") as fh:
  for path in paths:fh.write(f"file '{path.resolve()}'\nduration 0.8\n")
  fh.write(f"file '{paths[-1].resolve()}'\n")
 sr=48000;audio=np.zeros(int(19.2*sr),dtype=np.float32)
 for i in range(6):
  pos=int(i*3.2*sr);tt=np.arange(7000)/sr
  audio[pos:pos+7000]=.055*np.sin(2*np.pi*530*tt)*np.exp(-tt*28)
 import soundfile as sf
 sf.write(OUT/"sfx.wav",audio,sr)
 mp4=OUT/"cycle485_CI_SFX_ONLY_NOT_APPROVED.mp4"
 subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(concat),"-i",str(OUT/"sfx.wav"),"-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","20","-c:a","aac","-b:a","160k","-t","19.2","-movflags","+faststart",str(mp4)],check=True)
 subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(mp4),"-f","null","-"],check=True)
 print(mp4)
if __name__=="__main__":main()
