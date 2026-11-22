"""Review-only storyboard renderer. Original synthetic data, no voice claim."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DURATION=1080,1920,24,18
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[
("その入力、毎回やり直していませんか？","表記ゆれが確認作業を増やします"),
("BEFORE｜入力がバラバラ","株式会社ABC / (株)ABC / ABC"),
("AFTER｜ルールを統一","株式会社ABC → 株式会社ABC"),
("最後に人が確認","AIの提案は必ず目視でチェック"),
("3ステップで始める","①決める ②揃える ③確認する"),
]
def frame(t):
    index=min(4,int(t/3.6))
    progress=(t-index*3.6)/3.6
    im=Image.new("RGB",(W,H),(9,16,32))
    d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,52)
    small=ImageFont.truetype(FONT,37)
    d.rounded_rectangle((66,175,1014,1680),radius=45,fill=(20,33,54))
    d.text((110,300),"AI × 業務改善 / REVIEW ONLY",font=small,fill=(105,225,218))
    d.text((110,470),SCENES[index][0],font=f,fill="white")
    d.rounded_rectangle((110,670,970,1040),radius=26,fill=(29,43,64))
    if index in (1,2):
        rows=["株式会社ABC","(株)ABC","ABC"] if index==1 else ["株式会社ABC"]*3
        for j,label in enumerate(rows):
            y=708+j*104
            d.rounded_rectangle((147,y,927,y+82),radius=12,fill=(55,42,55) if index==1 else (30,72,64))
            d.text((173,y+13),label,font=small,fill="white")
            if j==min(2,int(progress*3)):
                d.rounded_rectangle((140,y-5,935,y+87),radius=14,outline=(70,213,195),width=6)
    else:
        d.text((151,815),"入力 → 整理 → 確認",font=small,fill=(184,232,222))
        x=160+int(680*progress)
        d.rounded_rectangle((x,950,x+55,970),radius=9,fill=(70,213,195))
    d.text((110,1150),SCENES[index][1],font=small,fill="white")
    d.text((110,1530),"※ 模擬データ / 人による確認が必要",font=small,fill=(173,189,205))
    d.rounded_rectangle((112,1595,968,1612),radius=8,fill=(64,82,99))
    d.rounded_rectangle((112,1595,112+int(856*progress),1612),radius=8,fill=(70,213,195))
    return im
def render(output):
    output=Path(output)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-an","-c:v","libx264","-preset","ultrafast","-crf","28","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(DURATION*FPS):
        p.stdin.write(frame(n/FPS).tobytes())
    p.stdin.close()
    if p.wait()!=0: raise RuntimeError("ffmpeg failed")
    return output
if __name__=="__main__":
    render("cycle1636_REVIEW_ONLY.mp4")
