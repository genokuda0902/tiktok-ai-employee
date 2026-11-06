"""Cycle1264 reusable storyboard renderer; review only. Requires Pillow and FFmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, math
SCENES=[("入力が長いほど","AIの回答は良くなる？","実は「条件の整理」が重要"),("目的を1行に","誰に・何を・どの形式で","3つに分けて伝える"),("最後に人が確認","数字・固有名詞・公開範囲","確認してから使おう")]
W,H,FPS=720,1280,15
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def render(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 frames=out/"frames";frames.mkdir(exist_ok=True)
 f=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
 for i in range(225):
  t=i/FPS;idx=min(2,int(t//5));local=t-idx*5
  im=Image.new("RGB",(W,H),(9,18,33));d=ImageDraw.Draw(im)
  for j in range(0,H,8):
   v=int(10+12*j/H);d.rectangle((0,j,W,j+8),fill=(v,v+10,v+24))
  d.rounded_rectangle((48,120,672,1150),radius=32,fill=(24,38,61),outline=(66,101,135),width=2)
  d.text((72,155),"AI WORKFLOW / 03",font=f(26),fill=(115,218,225))
  d.rounded_rectangle((72,220,648,236),radius=8,fill=(55,76,99))
  d.rounded_rectangle((72,220,72+int(576*t/15),236),radius=8,fill=(75,219,194))
  d.text((72,275),f"0{idx+1} / 03",font=f(34,True),fill=(100,225,207))
  for y,txt,size,b in [(395,SCENES[idx][0],48,True),(490,SCENES[idx][1],35,False)]:
   font=f(size,b);bb=d.textbbox((0,0),txt,font=font);d.text(((W-(bb[2]-bb[0]))/2,y),txt,font=font,fill="white")
  lift=int(10*math.sin(local*math.pi/5))
  d.rounded_rectangle((88,635-lift,632,870-lift),radius=24,fill=(35,64,88),outline=(80,154,176),width=3)
  txt=SCENES[idx][2];font=f(30,True);bb=d.textbbox((0,0),txt,font=font)
  d.text(((W-(bb[2]-bb[0]))/2,705-lift),txt,font=font,fill="white")
  d.text((80,1040),"保存前に内容をチェック",font=f(29),fill=(167,187,205))
  im.save(frames/f"{i:04d}.png")
 srt="\n\n".join(f"{i+1}\n00:00:{i*5:02d},000 --> 00:00:{(i+1)*5:02d},000\n{v[0]}。{v[1]}。{v[2]}。" for i,v in enumerate(SCENES))+"\n"
 (out/"captions.srt").write_text(srt,encoding="utf-8")
 subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(frames/"%04d.png"),"-c:v","libx264","-preset","veryfast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(out/"cycle1264_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__":render("output/cycle1264")
