"""Public-safe synthetic demo generator; no external assets or posting."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
SCENES=[("その集計、まだ手入力？","毎月の売上集計を確認"),("BEFORE","12,000 + 8,000 + 15,000 + 5,000"),("AFTER","=SUM(B2:B5) → 40,000円"),("最後に確認","元データ・範囲・合計値をチェック")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def render():
    ROOT.mkdir(parents=True,exist_ok=True)
    for i,(title,detail) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),(8,18,37));d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,120,680,1100),radius=30,fill=(19,39,65))
        d.text((65,280),title,font=ImageFont.truetype(FONT,46),fill="white")
        d.rounded_rectangle((65,440,655,860),radius=20,fill=(238,246,249))
        d.text((85,570),detail,font=ImageFont.truetype(FONT,25),fill=(20,60,80))
        d.text((65,1180),"REVIEW ONLY",font=ImageFont.truetype(FONT,25),fill="white")
        image=ROOT/f"scene{i}.png";im.save(image)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","30","-i",str(image),"-t","3","-c:v","libx264","-pix_fmt","yuv420p",str(ROOT/f"clip{i}.mp4")],check=True)
    (ROOT/"concat.txt").write_text("".join("file '"+str((ROOT/f"clip{i}.mp4").resolve())+"'\n" for i in range(4)))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(ROOT/"concat.txt"),"-c","copy","-movflags","+faststart",str(ROOT/"cycle1307_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__":render()
