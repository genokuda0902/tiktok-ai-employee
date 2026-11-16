"""Reproducible Japanese slide review. Audio deliberately fails closed."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
SCENES=[("AIへの指示、変えるだけ","目的を一文で伝える"),("悪い例","「資料を作って」だけ"),("良い例","「新人向けに3項目で」"),("最後に確認","数字と根拠は人が確認")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def render():
    clips=[]
    for i,(headline,subtitle) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),(11,20,38)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((44,140,676,1100),radius=35,fill=(23,39,63))
        d.rectangle((44,140,55,1100),fill=(54,202,218))
        d.text((72,410),headline,font=ImageFont.truetype(FONT,48),fill="white")
        d.text((88,700),subtitle,font=ImageFont.truetype(FONT,32),fill="white")
        d.text((75,1150),"REVIEW ONLY / 投稿未承認",font=ImageFont.truetype(FONT,25),fill="white")
        frame=ROOT/f"frame{i}.png"; im.save(frame)
        clip=ROOT/f"s{i}.mp4"; clips.append(clip)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","24","-i",str(frame),"-t","2","-c:v","libx264","-pix_fmt","yuv420p",str(clip)],check=True)
    concat=ROOT/"concat.txt"
    concat.write_text("".join("file '"+str(c)+"'\n" for c in clips))
    out=ROOT/"cycle1493_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(out)],check=True)
    return out
if __name__=="__main__":print(render())
