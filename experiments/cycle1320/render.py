from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
P=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
f=ImageFont.truetype(FONT,52); sm=ImageFont.truetype(FONT,32)
scenes=[("売上集計、まだ手作業？","BEFORE 毎日10分の集計"),("まず範囲を選択","B2:B6 をドラッグ"),("SUM関数を入力","=SUM(B2:B6)"),("合計が自動で更新","AFTER 集計の手間を減らす")]
for i,(head,sub) in enumerate(scenes):
 im=Image.new("RGB",(720,1280),(9,18,36)); d=ImageDraw.Draw(im)
 d.rounded_rectangle((38,105,682,1120),radius=35,fill=(24,39,65))
 d.text((65,165),head,font=f,fill="white"); d.text((65,255),sub,font=sm,fill=(93,225,220))
 d.rounded_rectangle((65,370,655,850),radius=16,fill=(242,246,251))
 d.rectangle((65,370,655,430),fill=(29,105,80)); d.text((90,381),"売上管理.xlsx",font=sm,fill="white")
 for j in range(5):
  y=450+j*70; d.line((90,y+57,625,y+57),fill=(195,205,215),width=2)
  d.text((110,y),f"{j+1}日",font=sm,fill=(34,50,68)); d.text((390,y),f"{(j+2)*1200:,}円",font=sm,fill=(34,50,68))
 if i>=2:
  d.rounded_rectangle((90,825,625,920),radius=10,fill=(217,244,236))
  d.text((120,839),"合計  24,000円",font=sm,fill=(10,105,80))
 d.text((65,1010),"架空データ / レビュー専用",font=sm,fill=(220,225,235))
 d.rectangle((65,1160,65+int(590*(i+1)/4),1172),fill=(64,218,207))
 im.save(P/f"s{i}.png")
with (P/"concat.txt").open("w") as o:
 for i in range(4): o.write(f"file '{P/f's{i}.png'}'\nduration 3\n")
 o.write(f"file '{P/'s3.png'}'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(P/"concat.txt"),"-vf","fps=30,format=yuv420p","-t","12","-c:v","libx264","-preset","ultrafast","-movflags","+faststart",str(P/"cycle1320_REVIEW_ONLY.mp4")],check=True)
