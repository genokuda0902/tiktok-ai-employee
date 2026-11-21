"""Synthetic, review-only vertical render with timed Japanese on-screen captions. No speech claim."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
SCENES=[("数字が合わない？","商品Ａ と 商品A","表記ゆれを確認"),("表記を統一","商品Ａ → 商品A","全角を半角へ"),("集計し直す","SUMIFで再集計","元データと照合")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def render():
    assert Path(FONT).exists()
    frames=ROOT/"frames";frames.mkdir(exist_ok=True)
    for i in range(216):
        index=min(i//72,2); title,example,caption=SCENES[index]
        im=Image.new("RGB",(720,1280),(9,18,35));d=ImageDraw.Draw(im)
        d.rounded_rectangle((36,125,684,990),radius=30,fill=(26,42,66))
        f=ImageFont.truetype(FONT,39);small=ImageFont.truetype(FONT,29)
        d.text((55,210),title,font=f,fill="white")
        d.rounded_rectangle((55,370,665,700),radius=18,fill=(239,247,251))
        d.text((80,490),example,font=f,fill=(20,48,65))
        d.rounded_rectangle((40,1035,670,1140),radius=18,fill=(0,0,0))
        d.text((60,1060),caption,font=small,fill="white")
        d.text((40,1180),"REVIEW ONLY / NO NARRATION",font=small,fill=(185,195,210))
        im.save(frames/f"{i:04d}.png")
    out=ROOT/"cycle1615_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","24","-i",str(frames/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    return out
if __name__=="__main__": print(render())
