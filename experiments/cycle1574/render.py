"""Review-only synthetic vertical video renderer. No narration: NEVER publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, tempfile
W,H,FPS,DURATION=540,960,24,10
SCENES=[("作業時間を見える化","現状を把握"),("作業を3つに分ける","入力・確認・連絡"),("時間のかかる作業","改善候補を選ぶ"),("改善前後を比較","数値は例示")]
def scene_index(seconds):
    return min(len(SCENES)-1,int(seconds/2.5))
def render(out):
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    with tempfile.TemporaryDirectory() as tmp:
        for frame in range(FPS*DURATION):
            t=frame/FPS; i=scene_index(t); progress=min(1,(t%2.5)/1.25)
            im=Image.new("RGB",(W,H),(9,17,33)); d=ImageDraw.Draw(im)
            d.rounded_rectangle((30,95,510,860),radius=28,fill=(23,39,63))
            d.text((55,160),SCENES[i][0],font=ImageFont.truetype(font,27),fill="white")
            d.text((55,230),SCENES[i][1],font=ImageFont.truetype(font,23),fill=(170,220,230))
            for j,(name,v) in enumerate([("入力",.83),("確認",.53),("連絡",.32)]):
                y=390+j*105
                d.text((60,y-32),name,font=ImageFont.truetype(font,22),fill="white")
                d.rounded_rectangle((60,y,460,y+22),radius=10,fill=(52,72,96))
                width=max(1,int(400*v*progress))
                d.rounded_rectangle((60,y,60+width,y+22),radius=10,fill=(48,211,192))
            d.text((55,795),"架空データ / REVIEW ONLY",font=ImageFont.truetype(font,18),fill="white")
            im.save(f"{tmp}/{frame:04d}.png")
        subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{tmp}/%04d.png","-f","lavfi","-i","anullsrc=channel_layout=mono:sample_rate=44100","-t",str(DURATION),"-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",str(out)],check=True)
if __name__=="__main__":
    render(Path("review_only.mp4"))
