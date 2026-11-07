"""Review-only synthetic UI renderer. Reimplementation, not original v33."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("AIの回答、すぐ提出？","まず3つ確認"),("出典を確認","根拠のURLや資料を開く"),("日付を確認","古い情報を混ぜない"),("最後は人が判断","確認してから共有する")]
def render():
    clips=[]
    for i,(title,detail) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),"#0b1220"); d=ImageDraw.Draw(im)
        large=ImageFont.truetype(FONT,76); mid=ImageFont.truetype(FONT,46); small=ImageFont.truetype(FONT,30)
        d.rounded_rectangle((72,180,1008,1650),radius=44,fill="#16243a")
        d.rounded_rectangle((120,250,960,350),radius=24,fill="#23577b")
        d.text((150,275),"AI WORKFLOW / REVIEW",font=small,fill="white")
        d.text((130,470),title,font=large,fill="white")
        d.text((130,640),detail,font=mid,fill="#d2e8f3")
        for j,t in enumerate(["情報の出典","更新された日付","最終確認"]):
            y=860+j*160; d.rounded_rectangle((130,y,940,y+125),radius=18,fill="#223650")
            d.ellipse((160,y+43,195,y+78),fill="#37cfa5" if j<i else "#62758b")
            d.text((220,y+35),t,font=mid,fill="white")
        d.text((110,1770),"レビュー専用｜実画面ではありません",font=small,fill="#b9c8d9")
        png=ROOT/f"scene_{i}.png"; im.save(png)
        clip=ROOT/f"clip_{i}.mp4"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","24","-i",str(png),"-t","3","-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p",str(clip)],check=True)
        clips.append(clip)
    (ROOT/"concat.txt").write_text("".join(f"file '{p.name}'\n" for p in clips))
    out=ROOT/"cycle1285_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(ROOT/"concat.txt"),"-c","copy","-movflags","+faststart",str(out)],check=True)
    (ROOT/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{a}。{b}\n\n" for i,(a,b) in enumerate(SCENES)),encoding="utf-8")
    return out
if __name__=="__main__": print(render())
