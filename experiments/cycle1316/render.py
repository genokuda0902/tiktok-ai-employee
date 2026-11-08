"""Review-only 1080p Excel storyboard. Requires Pillow and FFmpeg. No audio is claimed."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
 ("Excelの集計、まだ手入力？","3秒で合計を出す方法","BEFORE"),
 ("まず合計セルを選択","B5をクリック","STEP 1"),
 ("SUM関数を入力","=SUM(B2:B4)","STEP 2"),
 ("Enterで集計完了","1200 + 850 + 950 = 3000","AFTER"),
 ("まずは1つ試してみよう","架空データによる操作イメージ","SAVE")]
def render():
 for i,(heading,detail,tag) in enumerate(SCENES):
  im=Image.new("RGB",(1080,1920),(9,17,35));d=ImageDraw.Draw(im)
  d.rounded_rectangle((64,150,1016,1720),radius=48,fill=(21,35,57))
  d.rounded_rectangle((96,198,984,280),radius=20,fill=(20,105,128))
  d.text((130,213),tag,font=ImageFont.truetype(BOLD,38),fill="white")
  d.text((105,355),heading,font=ImageFont.truetype(BOLD,55),fill="white")
  d.rounded_rectangle((105,555,975,1130),radius=25,fill=(244,249,250))
  for j,t in enumerate(["項目                 金額","A                      1,200","B                         850","C                         950","合計                    ?" if i<3 else "合計                  3,000"]):
   y=620+j*90;d.text((145,y),t,font=ImageFont.truetype(FONT,39),fill=(15,36,48))
   if j<4:d.line((130,y+69,950,y+69),fill=(210,223,226),width=2)
  d.rounded_rectangle((105,1200,975,1390),radius=28,fill=(36,69,95))
  d.text((140,1252),detail,font=ImageFont.truetype(BOLD,42),fill="white")
  d.text((110,1580),"REVIEW ONLY  |  NOT APPROVED",font=ImageFont.truetype(FONT,31),fill=(195,210,220))
  im.save(ROOT/f"frame{i}.png")
 with (ROOT/"frames.txt").open("w") as f:
  for i in range(5):f.write(f"file 'frame{i}.png'\nduration 3\n")
  f.write("file 'frame4.png'\n")
 subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(ROOT/"frames.txt"),"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","24","-t","15","-movflags","+faststart",str(ROOT/"cycle1316_REVIEW_ONLY.mp4")],check=True)
 (ROOT/"cycle1316.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{heading}。{detail}\n\n" for i,(heading,detail,_) in enumerate(SCENES)),encoding="utf-8")
if __name__=="__main__":render()
