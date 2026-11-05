"""Cycle1246: public-safe synthetic spreadsheet scene renderer (reimplementation)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
SCENES=[("BEFORE","集計に10分かかる","120 と 180 を手入力","120 + 180 = ?"),("ACTION","SUM関数で自動計算","=SUM(B2:B3) を入力","B2 120 / B3 180"),("AFTER","合計は300","入力した数値から自動集計","120 + 180 = 300")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def render(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,(stage,headline,caption,formula) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),"#081626");d=ImageDraw.Draw(im)
        f=lambda n:ImageFont.truetype(FONT,n)
        d.rounded_rectangle((35,50,685,300),20,fill="#163451")
        d.text((60,80),stage,font=f(36),fill="#63dce8")
        d.text((60,170),headline,font=f(42),fill="white")
        d.rounded_rectangle((35,350,685,940),20,fill="#f6f8fb")
        d.rectangle((35,350,685,420),fill="#176a54")
        d.text((60,365),"集計シート",font=f(30),fill="white")
        for y,label,value in [(480,"A","120"),(600,"B","180"),(720,"合計","?" if i==0 else "=SUM(B2:B3)" if i==1 else "300")]:
            d.text((80,y),label,font=f(34),fill="#1b3548")
            d.text((260,y),value,font=f(32),fill="#08775e")
            d.line((60,y+65,660,y+65),fill="#c9d5df",width=2)
        d.text((55,1000),caption,font=f(29),fill="white")
        d.text((55,1080),formula,font=f(27),fill="#63dce8")
        d.text((55,1170),"REVIEW ONLY / 投稿未承認",font=f(23),fill="#f4b8b8")
        png=output/f"scene{i}.png";im.save(png)
        clip=output/f"clip{i}.mp4"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","24","-i",str(png),"-t","5","-vf","format=yuv420p","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",str(clip)],check=True)
        clips.append(clip)
    playlist=output/"concat.txt";playlist.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
    mp4=output/"cycle1246_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(playlist),"-c","copy","-movflags","+faststart",str(mp4)],check=True)
    return mp4
if __name__=="__main__":print(render("output/cycle1246"))
