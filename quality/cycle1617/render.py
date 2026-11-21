"""cycle1617: self-contained 15-second caption-safe synthetic demo. Review only."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("毎月の集計、まだ手作業？","BEFORE｜表記ゆれで集計ミス"),("商品Ａ と 商品A","同じ商品なのに別々に集計"),("表記を統一 → SUMIF","AFTER｜同じ商品として正しく集計"),("集計結果を確認","保存してあとで試す")]
def render():
    frames=ROOT/"frames";frames.mkdir(exist_ok=True)
    for i in range(360):
        scene=min(i//90,3);title,subtitle=SCENES[scene]
        im=Image.new("RGB",(720,1280),"#0a1425");d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,130,680,1020),radius=30,fill="#172a43")
        d.rectangle((40,130,680,142),fill="#34d6bd")
        f1=ImageFont.truetype(FONT,44);f2=ImageFont.truetype(FONT,28)
        d.text((62,200),title,font=f1,fill="white")
        for r,label in enumerate(["商品Ａ    12件","商品A      8件","商品Ｂ    10件","合計       30件","確認       OK"]):
            y=360+r*95
            d.rounded_rectangle((65,y,655,y+74),radius=10,fill="#27586b" if r==scene else "#23374f")
            d.text((84,y+15),label,font=f2,fill="white")
        d.rounded_rectangle((40,1060,680,1170),radius=20,fill="#101b31")
        d.text((60,1090),subtitle,font=f2,fill="white")
        d.rectangle((40,1210,40+int(640*(i+1)/360),1220),fill="#34d6bd")
        im.save(frames/f"{i:04d}.png")
    out=ROOT/"cycle1617_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","24","-i",str(frames/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    return out
if __name__=="__main__": print(render())
