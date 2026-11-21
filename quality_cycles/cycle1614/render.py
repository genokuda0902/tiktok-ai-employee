"""Self-contained synthetic REVIEW ONLY render; no third-party media or user data."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("入力の表記ゆれ","商品Ａ と 商品A","集計結果がずれる原因"),("統一してから集計","商品Ａ → 商品A","同じ名前にそろえる"),("集計結果を確認","SUMIF で集計","数字は最後に目視確認")]
def render():
    assert Path(FONT).exists(), "Japanese Noto font required"
    frames=ROOT/"frames"; frames.mkdir(exist_ok=True)
    for i in range(192):
        title,main,sub=SCENES[min(i//64,2)]
        im=Image.new("RGB",(720,1280),(9,17,33));d=ImageDraw.Draw(im)
        d.rounded_rectangle((35,135,685,1060),radius=35,fill=(25,38,60))
        d.rectangle((35,135,685,148),fill=(45,210,195))
        d.text((62,205),title,font=ImageFont.truetype(BOLD,46),fill="white")
        d.rounded_rectangle((62,365,658,730),radius=25,fill=(240,246,251))
        d.text((84,480),main,font=ImageFont.truetype(BOLD,37),fill=(20,40,65))
        d.text((62,800),sub,font=ImageFont.truetype(FONT,34),fill=(220,234,244))
        d.rounded_rectangle((62,952,658,968),radius=8,fill=(55,72,94))
        progress=int(596*((i%64)/64))
        if progress:d.rounded_rectangle((62,952,62+progress,968),radius=8,fill=(45,210,195))
        d.text((62,1125),"REVIEW ONLY  |  音声未実装",font=ImageFont.truetype(FONT,24),fill=(180,190,205))
        im.save(frames/f"{i:04d}.png")
    out=ROOT/"cycle1614_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","24","-i",str(frames/"%04d.png"),"-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    return out
if __name__=="__main__":print(render())
