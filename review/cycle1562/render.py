"""Original synthetic review-only video. No external media, no Japanese narration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
W,H,FPS,DUR=720,1280,24,12
STEPS=[("まず、合計を見てみよう","4つの数字をまとめて計算"),("B2〜B5を選択","合計したいセルを指定"),("SUM関数を入力","=SUM(B2:B5)"),("結果は10,000円","計算できたら数字を確認")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def frame(t):
 im=Image.new("RGB",(W,H),"#0a1326");d=ImageDraw.Draw(im)
 step=min(int(t//3),3); title,sub=STEPS[step]
 d.rounded_rectangle((34,58,686,152),radius=22,fill="#172b46")
 d.text((57,79),"Excel 合計を12秒で解説",font=font(39,True),fill="white")
 d.rounded_rectangle((34,190,686,355),radius=24,fill="#123d46")
 d.text((58,218),title,font=font(39,True),fill="#f2fff9")
 d.text((58,288),sub,font=font(27),fill="#a9e5d8")
 d.rounded_rectangle((34,405,686,915),radius=20,fill="#f7fafc")
 d.rectangle((34,405,686,470),fill="#15744f")
 d.text((62,418),"売上集計.xlsx  /  Sheet1",font=font(24,True),fill="white")
 for x,c in [(68,"A"),(180,"B"),(365,"C")]:d.text((x+18,487),c,font=font(25,True),fill="#3c4855")
 for i,v in enumerate(["1,000","2,000","3,000","4,000"]):
  y=541+i*66;d.line((54,y+56,666,y+56),fill="#cbd5df",width=2)
  d.text((67,y+8),str(i+2),font=font(22),fill="#5c6977")
  d.text((205,y+8),v,font=font(29,True),fill="#172b46")
 d.line((180,472,180,874),fill="#cbd5df",width=2)
 d.line((365,472,365,874),fill="#cbd5df",width=2)
 if step>=1:d.rounded_rectangle((185,543,358,797),radius=5,outline="#08a86b",width=5)
 if step>=2:
  d.rounded_rectangle((66,821,649,882),radius=8,fill="#e4f7eb")
  d.text((80,830),"=SUM(B2:B5)",font=font(26,True),fill="#0d6040")
 if step>=3:
  d.rounded_rectangle((160,965,560,1055),radius=17,fill="#13a475")
  d.text((200,984),"合計  10,000円",font=font(36,True),fill="white")
 d.rounded_rectangle((34,1092,686,1183),radius=19,fill="#1c2c46")
 d.text((60,1111),sub,font=font(30,True),fill="white")
 d.rounded_rectangle((34,1215,686,1227),radius=6,fill="#30405b")
 d.rounded_rectangle((34,1215,34+int(652*t/DUR),1227),radius=6,fill="#25d6a1")
 return im
def render(outdir=Path(".")):
 outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
 target=outdir/"cycle1562_REVIEW_ONLY.mp4"
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-t",str(DUR),"-c:v","libx264","-preset","ultrafast","-crf","26","-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart",str(target)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(FPS*DUR):p.stdin.write(frame(n/FPS).tobytes())
 p.stdin.close()
 if p.wait():raise RuntimeError("ffmpeg encode failed")
 srt="".join(f"{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{a}。{b}。\n\n" for i,(a,b) in enumerate(STEPS))
 (outdir/"captions_ja.srt").write_text(srt,encoding="utf-8")
 return target
if __name__=="__main__":print(render())
