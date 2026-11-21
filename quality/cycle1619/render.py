"""Cycle1619 public-safe silent storyboard reimplementation; NOT approved for publishing."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("毎日の集計、まだ手作業？","表記ゆれを先に見つける"),("STEP 1｜入力を確認","商品Ａ と 商品A を検出"),("STEP 2｜名前を統一","同じ商品名にそろえる"),("STEP 3｜結果を照合","集計結果は必ず人が確認")]
def render():
    ROOT.mkdir(exist_ok=True)
    for i,(title,sub) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),(10,19,36)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,125,680,1110),radius=34,fill=(23,40,66))
        d.rectangle((40,125,52,1110),fill=(24,206,189))
        d.text((78,200),title,font=ImageFont.truetype(BOLD,39),fill="white")
        d.rounded_rectangle((78,385,642,780),radius=24,fill=(235,243,249))
        for j,(a,b) in enumerate([("商品Ａ","12"),("商品A","8"),("合計","20")]):
            y=430+j*100
            d.text((110,y),a,font=ImageFont.truetype(FONT,35),fill=(26,48,72))
            d.text((540,y),b,font=ImageFont.truetype(BOLD,35),fill=(26,48,72))
            d.line((105,y+72,610,y+72),fill=(176,195,207),width=2)
        d.text((78,870),sub,font=ImageFont.truetype(FONT,31),fill=(233,242,250))
        d.text((78,1030),f"{i+1} / 4   •   REVIEW ONLY",font=ImageFont.truetype(FONT,23),fill=(100,212,200))
        im.save(ROOT/f"frame{i}.png")
    with (ROOT/"concat.txt").open("w") as f:
        for i in range(4): f.write(f"file '{ROOT}/frame{i}.png'\\nduration 2.5\\n".replace("\\n","\n"))
        f.write(f"file '{ROOT}/frame3.png'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(ROOT/"concat.txt"),"-vf","fps=24,format=yuv420p","-c:v","libx264","-crf","23","-movflags","+faststart",str(ROOT/"cycle1619_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__": render()
