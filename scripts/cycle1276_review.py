"""Review-only, original graphic renderer. No narration; not publication-ready."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
OUT=Path("output/cycle1276"); OUT.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("AIの回答、そのまま提出？","確認しないと、間違いが残る。"),("BEFORE","この情報をまとめて"),("AFTER","根拠・日付・不明点も示して"),("最後は人が確認","出典を開いて数字を照合する")]
for i,(title,detail) in enumerate(SCENES):
    im=Image.new("RGB",(720,1280),(9,17,34)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((42,90,678,1190),radius=38,fill=(23,38,65))
    d.rectangle((42,90,42+(i+1)*159,101),fill=(50,211,185))
    d.text((75,165),f"AI WORKFLOW / 0{i+1}",font=ImageFont.truetype(FONT,29),fill=(70,227,198))
    d.text((75,320),title,font=ImageFont.truetype(BOLD,44),fill="white")
    d.rounded_rectangle((75,700,645,940),radius=22,fill=(36,56,84))
    d.text((95,745),detail,font=ImageFont.truetype(FONT,27),fill="white")
    d.text((75,1080),"REVIEW ONLY / NOT APPROVED",font=ImageFont.truetype(FONT,21),fill=(174,193,213))
    im.save(OUT/f"scene{i}.png")
with (OUT/"list.txt").open("w") as f:
    for i in range(4): f.write(f"file '{(OUT/f'scene{i}.png').resolve()}'\nduration 3\n")
    f.write(f"file '{(OUT/'scene3.png').resolve()}'\n")
(OUT/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{title}\n\n" for i,(title,_) in enumerate(SCENES)),encoding="utf-8")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(OUT/"list.txt"),"-t","12","-r","24","-c:v","libx264","-pix_fmt","yuv420p",str(OUT/"review.mp4")],check=True)
