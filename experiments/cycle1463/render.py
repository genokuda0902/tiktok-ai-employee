"""Review-only motion storyboard. Requires pillow, ffmpeg, Noto CJK font."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
O=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
F=lambda n:ImageFont.truetype(FONT,n)
SCENES=[("01 / PROBLEM","毎日の転記作業","同じ情報を何度も入力していませんか？"),("02 / ACTION","まず3項目を整理","入力元・出力先・確認担当"),("03 / DEMO","作業の流れを見える化","入力 → 確認 → 転記"),("04 / CHECK","最後は人が確認","個人情報を含めず、小さく試す")]
for i,(tag,title,sub) in enumerate(SCENES):
 im=Image.new("RGB",(1080,1920),"#091422"); d=ImageDraw.Draw(im)
 d.rounded_rectangle((65,210,1015,1690),radius=38,fill="#14283a",outline="#366c86",width=3)
 d.rectangle((65,210,1015,226),fill="#39c4c7")
 d.text((110,310),tag,font=F(48),fill="#65e5df")
 d.text((110,485),title,font=F(69),fill="white")
 d.text((110,645),sub,font=F(35),fill="#d6e7ef")
 for j,label in enumerate(["INPUT","CHECK","OUTPUT"]):
  x=115+j*293
  d.rounded_rectangle((x,980,x+245,1160),radius=22,fill="#24465b",outline="#61b9c0",width=3)
  d.text((x+26,1040),label,font=F(29),fill="white")
  if j<2:d.text((x+250,1035),"›",font=F(65),fill="#66e6dc")
 d.text((110,1500),"REVIEW ONLY  /  音声未実装",font=F(28),fill="#e8ad83")
 d.rounded_rectangle((110,1590,110+(i+1)*200,1604),radius=5,fill="#61e5df")
 im.save(O/f"scene{i}.png")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","15","-i",str(O/f"scene{i}.png"),"-t","3","-vf","zoompan=z='min(zoom+0.0006,1.04)':d=1:s=1080x1920:fps=15,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","27","-an",str(O/f"part{i}.mp4")],check=True)
(O/"concat.txt").write_text("".join(f"file 'part{i}.mp4'\n" for i in range(4)))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(O/"concat.txt"),"-c","copy","-movflags","+faststart",str(O/"cycle1463_REVIEW_ONLY.mp4")],check=True)
