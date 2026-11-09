"""Reproducible synthetic 5-scene review video. No narration; never publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
SCENES=[("手入力で集計してない？","毎月の合計、関数なら一瞬"),("売上の列を確認","B2からB5を合計します"),("=SUM(B2:B5)","合計セルに関数を入力"),("合計 30,000円","架空の売上表で確認"),("保存して試そう","数字は架空のサンプルです")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def render():
    clips=[]
    for i,(title,detail) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),(8,18,33));d=ImageDraw.Draw(im)
        d.rounded_rectangle((70,160,1010,1740),radius=40,fill=(18,36,58))
        f=ImageFont.truetype(FONT,56);small=ImageFont.truetype(FONT,35)
        d.text((120,320),title,font=f,fill="white")
        d.text((120,510),detail,font=small,fill=(195,224,232))
        for j,v in enumerate(("12,000","8,000","6,000","4,000")):
            y=760+j*120;d.rounded_rectangle((120,y,950,y+105),radius=12,fill=(32,65,80))
            d.text((170,y+25),f"担当{j+1}",font=small,fill="white")
            d.text((650,y+25),v,font=small,fill=(90,225,211))
        d.text((120,1530),"架空データ｜公開前レビュー",font=small,fill="white")
        img=ROOT/f"frame{i}.png";im.save(img)
        clip=ROOT/f"clip{i}.mp4"
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-i",str(img),"-t","3","-vf","format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","27","-an",str(clip)],check=True)
        clips.append(clip)
    manifest=ROOT/"concat.txt";manifest.write_text("".join(f"file '{p}'\n" for p in clips))
    out=ROOT/"review_only.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(manifest),"-c","copy","-movflags","+faststart",str(out)],check=True)
    return out
if __name__=="__main__":print(render())
