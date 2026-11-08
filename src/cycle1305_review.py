"""Reproducible review-only Excel demo. Requires Pillow and ffmpeg. No narration; NEVER publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
OUT=Path("output/cycle1305"); OUT.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
("その集計、まだ手入力？","毎日の売上確認を時短"),
("BEFORE｜手作業","4件を電卓で足す"),
("Excelで範囲を選択","B2:B5 をまとめて選択"),
("SUM関数を入力","=SUM(B2:B5)"),
("AFTER｜合計が一瞬で","40,000 円"),
("明日から試してみよう","保存してあとで確認")]
def render():
    clips=[]
    for i,(heading,sub) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),(8,17,34)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((35,120,685,1130),radius=38,fill=(22,37,62),outline=(54,98,132),width=3)
        d.rounded_rectangle((58,160,662,230),radius=20,fill=(22,106,133))
        d.text((82,170),"AI × Excel  |  仕事の時短",font=ImageFont.truetype(BOLD,30),fill="white")
        d.text((72,290),heading,font=ImageFont.truetype(BOLD,44),fill="white")
        d.text((75,420),sub,font=ImageFont.truetype(FONT,33),fill=(170,235,244))
        for k,v in enumerate(["商品 A      12,000","商品 B        8,000","商品 C      15,000","商品 D        5,000"]):
            y=550+k*90; d.rounded_rectangle((80,y,640,y+75),radius=9,fill=(35,56,81))
            d.text((105,y+15),v,font=ImageFont.truetype(FONT,30),fill="white")
        if i>=3:
            d.rounded_rectangle((80,945,640,1035),radius=12,fill=(13,111,100))
            d.text((108,962),"合計  40,000 円",font=ImageFont.truetype(BOLD,38),fill="white")
        d.text((75,1150),f"{i+1:02d} / 06   ・  REVIEW ONLY",font=ImageFont.truetype(FONT,24),fill=(152,175,194))
        image=OUT/f"scene{i}.png"; im.save(image)
        clip=OUT/f"part{i}.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(image),"-t","3","-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",str(clip)],check=True)
        clips.append(clip)
    listing=OUT/"concat.txt"; listing.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))
    result=OUT/"cycle1305_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy","-movflags","+faststart",str(result)],check=True)
    (OUT/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{a}\n\n" for i,(a,b) in enumerate(SCENES)),encoding="utf8")
    return result
if __name__=="__main__": print(render())
