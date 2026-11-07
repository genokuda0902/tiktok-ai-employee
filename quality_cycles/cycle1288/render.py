"""Review-only 1080x1920 Japanese caption renderer. Requires Pillow and FFmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
D=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("AIの答え、\nそのまま使う？","まず3つだけ確認"),("01  出典","情報の根拠を確かめる"),("02  日付","古い情報を見逃さない"),("03  最終判断","公開前に人が確認する")]
def render():
    D.mkdir(parents=True,exist_ok=True)
    for i,(head,sub) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),(10,17,32)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((65,230,1015,1660),radius=50,fill=(22,37,61),outline=(62,104,140),width=3)
        d.rounded_rectangle((110,320,970,335),radius=6,fill=(61,204,194))
        d.text((120,420),head,font=ImageFont.truetype(FONT,88),fill="white",spacing=24)
        d.text((120,940),sub,font=ImageFont.truetype(FONT,50),fill=(160,230,225))
        d.text((120,1510),f"CHECK  {i+1:02d} / 04",font=ImageFont.truetype(FONT,36),fill=(180,193,209))
        im.save(D/f"{i}.png")
    (D/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{h.replace(chr(10),' ')}。{s}\n\n" for i,(h,s) in enumerate(SCENES)),encoding="utf-8")
    for i in range(4):
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(D/f"{i}.png"),"-t","3","-vf","scale=1080:1920,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","25","-an",str(D/f"{i}.mp4")],check=True)
    (D/"concat.txt").write_text("".join(f"file '{i}.mp4'\n" for i in range(4)))
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(D/"concat.txt"),"-c","copy","-movflags","+faststart",str(D/"cycle1288_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__": render()
