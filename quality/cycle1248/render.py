"""Review-only 3-scene video generator. Synthetic data; no narration."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES = [
    ("BEFORE", "毎回、手入力していませんか？", "120 + 180 = ?"),
    ("ACTION", "SUM関数で自動計算", " = SUM(A1:A2)"),
    ("AFTER", "結果は 300", "入力ミスを減らす第一歩"),
]
def render(root=ROOT):
    root.mkdir(parents=True, exist_ok=True)
    for i, (tag, headline, detail) in enumerate(SCENES):
        im = Image.new("RGB", (720,1280), "#081322")
        d = ImageDraw.Draw(im)
        f = lambda n: ImageFont.truetype(FONT,n)
        d.rounded_rectangle((48,130,672,1130),radius=38,fill="#14253a",outline="#36516b",width=3)
        d.text((75,185),tag,font=f(43),fill="#56e0c0")
        d.rounded_rectangle((75,300,645,680),radius=20,fill="#f4f7fc")
        for y in (370,440,510,580): d.line((98,y,625,y),fill="#c8d4e2",width=2)
        for x in (270,450): d.line((x,320,x,660),fill="#c8d4e2",width=2)
        d.text((115,330),"A",font=f(25),fill="#304458")
        d.text((300,330),"B",font=f(25),fill="#304458")
        d.text((115,400),"120",font=f(32),fill="#243a53")
        d.text((115,470),"180",font=f(32),fill="#243a53")
        if i==1: d.text((285,540),"SUM",font=f(29),fill="#1b806a")
        if i==2: d.text((295,540),"300",font=f(45),fill="#118365")
        d.text((75,755),headline,font=f(33),fill="white")
        d.text((75,845),detail,font=f(29),fill="#82dccc")
        d.text((75,1020),"架空データ / REVIEW ONLY",font=f(22),fill="#9eb1c4")
        im.save(root/f"scene{i}.png")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y"]
    for i in range(3):
        cmd += ["-loop","1","-framerate","24","-t","4","-i",str(root/f"scene{i}.png")]
    filters = "".join(f"[{i}:v]scale=720:1280,format=yuv420p,setsar=1[v{i}];" for i in range(3))
    filters += "[v0][v1][v2]concat=n=3:v=1:a=0[out]"
    output=root/"cycle1248_REVIEW_ONLY.mp4"
    subprocess.run(cmd+["-filter_complex",filters,"-map","[out]","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(output)],check=True)
    return output
if __name__=="__main__": render()
