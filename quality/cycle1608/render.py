"""Synthetic review-only vertical MP4: no speech and no confidential assets."""
from pathlib import Path
import argparse, subprocess
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=720,1280,24
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("集計ミス、まだ手で探す？","入力→検算を15秒で見せる"),("まず表を確認","売上データは架空の例です"),("SUMIFで集計","条件に一致する値だけを合計"),("結果を検算","12件 − 4件 = 残り8件"),("保存して次回試そう","公開前に必ず人が確認")]
def frame(t):
 i=min(int(t/3),4); local=t-i*3
 im=Image.new("RGB",(W,H),(8,17,34));d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,16),fill=(20,191,179))
 d.text((48,72),"AI × 仕事効率化",font=ImageFont.truetype(REG,28),fill=(106,226,215))
 d.text((48,160),SCENES[i][0],font=ImageFont.truetype(FONT,47),fill="white")
 d.text((48,244),SCENES[i][1],font=ImageFont.truetype(REG,28),fill=(200,213,230))
 d.rounded_rectangle((45,365,675,910),radius=25,fill=(21,36,57),outline=(61,88,112),width=2)
 if i in (1,2,3):
  d.text((76,405),"架空データ / 月次集計",font=ImageFont.truetype(REG,26),fill=(230,240,245))
  for r,(name,n) in enumerate([("A班",12),("B班",4),("残数",8)]):
   y=490+r*112;d.text((82,y),name,font=ImageFont.truetype(FONT,30),fill="white")
   d.rounded_rectangle((235,y+7,615,y+45),radius=12,fill=(43,59,78))
   p=min(1,max(0,(local-.25)/1.5))
   d.rounded_rectangle((235,y+7,235+int((n/12)*380*p),y+45),radius=12,fill=(24,196,176) if r<2 else (243,176,74))
  if i==2:d.text((83,825),"=SUMIF(条件範囲, 条件, 合計範囲)",font=ImageFont.truetype(REG,21),fill=(255,220,145))
 else:
  d.text((84,550),"BEFORE  →  AFTER",font=ImageFont.truetype(FONT,36),fill=(250,207,115))
  d.text((84,655),"確認 → 集計 → 検算",font=ImageFont.truetype(REG,32),fill="white")
 d.rounded_rectangle((45,1000,675,1104),radius=20,fill=(37,54,75))
 d.text((70,1026),f"{i+1}/5  {SCENES[i][0]}",font=ImageFont.truetype(REG,28),fill="white")
 d.rectangle((45,1160,675,1170),fill=(56,72,88))
 d.rectangle((45,1160,45+int(630*t/15),1170),fill=(28,206,182))
 d.text((48,1202),"REVIEW ONLY / 音声未実装",font=ImageFont.truetype(REG,19),fill=(183,193,210))
 return im
def render(out):
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","26","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for k in range(15*FPS):p.stdin.write(frame(k/FPS).tobytes())
 finally:p.stdin.close()
 if p.wait():raise RuntimeError("ffmpeg failed")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--out",default="cycle1608_REVIEW_ONLY.mp4");render(a.parse_args().out)
