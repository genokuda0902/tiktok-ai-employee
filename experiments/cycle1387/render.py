"""Review-only synthetic video; no narration. Requires pillow, ffmpeg, Noto CJK."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json, argparse
P=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
 ("集計に時間をかけていませんか？","4件の売上を、SUM関数で合計"),
 ("まず数字を確認","2,400 + 3,100 + 4,200 + 2,700"),
 ("合計セルに入力","=SUM(B2:B5)"),
 ("結果は12,400円","保存してあとで試そう"),
]
def render(out, size=(720,1280), fps=20, seconds=8):
 w,h=size
 font=lambda s,b=False:ImageFont.truetype(BOLD if b else FONT,max(12,round(s*w/720)))
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(fps),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","25","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(fps*seconds):
  idx=min(3,n//(fps*2)); progress=(n+1)/(fps*seconds)
  im=Image.new("RGB",(w,h),"#0b1628");d=ImageDraw.Draw(im)
  def rect(coords,fill,r=0):
   box=tuple(round(v*w/720) for v in coords) if w==h*720/1280 else (round(coords[0]*w/720),round(coords[1]*h/1280),round(coords[2]*w/720),round(coords[3]*h/1280))
   d.rounded_rectangle(box,radius=round(r*w/720),fill=fill)
  def txt(x,y,t,s,c,b=False):
   d.text((round(x*w/720),round(y*h/1280)),t,font=font(s,b),fill=c)
  rect((35,85,685,1100),"#17283c",24)
  txt(62,120,"EXCEL  /  時短テクニック",29,"#6de4bb",True)
  txt(55,240,SCENES[idx][0],32,"#ffffff",True)
  rect((55,390,665,850),"#f8fafc",15)
  rect((75,415,645,475),"#d0eee0")
  txt(94,423,"行",24,"#164e3c",True);txt(410,423,"売上",24,"#164e3c",True)
  for i,val in enumerate(["2,400","3,100","4,200","2,700"]):
   y=490+i*64;txt(96,y,str(i+2),23,"#475569");txt(420,y,val,24,"#17283c")
  txt(96,764,"6  合計",24,"#17283c",True)
  if idx>=2:txt(370,764,"=SUM(B2:B5)" if idx==2 else "12,400",21,"#166534",True)
  rect((55,900,665,1000),"#26435c",13)
  txt(74,929,SCENES[idx][1],25,"#ffffff",True)
  rect((55,1050,665,1066),"#334155",7)
  rect((55,1050,55+610*progress,1066),"#54ddb0",7)
  txt(55,1150,"REVIEW ONLY / 未承認・投稿禁止",22,"#ffb4bd")
  proc.stdin.write(im.tobytes())
 proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError("ffmpeg failed")
 return out
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--out",default=str(P/"cycle1387_REVIEW_ONLY.mp4"));a.add_argument("--width",type=int,default=720);args=a.parse_args()
 path=render(args.out,(args.width,round(args.width*16/9)))
 print(path)
