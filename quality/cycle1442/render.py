"""Reimplementation: synthetic REVIEW ONLY video, never auto-publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
STAGES=[("① 課題","毎回、合計を手入力？","1,200 + 2,300 + 3,200"),("② 解決","数式を一度入力","=SUM(B2:B4)"),("③ 結果","合計 6,700 を確認","数字は必ず検算しよう")]
def render():
    ROOT.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,(heading,title,detail) in enumerate(STAGES):
        im=Image.new("RGB",(540,960),"#0b1626"); d=ImageDraw.Draw(im)
        font=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
        d.rounded_rectangle((22,110,518,740),radius=24,fill="#eaf1f5")
        d.rounded_rectangle((40,180,500,590),radius=18,fill="#ffffff")
        d.text((34,35),"AI × 仕事術｜実演イメージ",font=font(25,True),fill="white")
        d.text((55,144),heading,font=font(29,True),fill="#0d4765")
        d.text((58,260),title,font=font(25,True),fill="#122b3f")
        d.rounded_rectangle((58,385,482,470),radius=10,fill="#d5eee8")
        d.text((70,404),detail,font=font(23,True),fill="#075f56")
        d.rounded_rectangle((25,772,515,860),radius=14,fill="#1b4155")
        d.text((42,795),title,font=font(24,True),fill="white")
        d.text((28,902),"REVIEW ONLY｜ナレーション未実装",font=font(17),fill="#f6c6a2")
        img=ROOT/f"scene_{i}.png"; im.save(img)
        clip=ROOT/f"scene_{i}.mp4"
        subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-loop","1","-framerate","24","-i",str(img),"-t","3","-vf","scale=1080:1920,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","23",str(clip)],check=True)
        clips.append(clip)
    lst=ROOT/"concat.txt";lst.write_text("".join(f"file '{p.name}'\n" for p in clips))
    out=ROOT/"cycle1442_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-c","copy","-movflags","+faststart",str(out)],check=True,cwd=ROOT)
    (ROOT/"captions.srt").write_text("1\n00:00:00,000 --> 00:00:03,000\n毎回、合計を手入力？\n\n2\n00:00:03,000 --> 00:00:06,000\n数式を一度入力\n\n3\n00:00:06,000 --> 00:00:09,000\n合計 6,700 を確認\n",encoding="utf-8")
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    return out
if __name__=="__main__":print(render())
