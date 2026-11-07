"""Review-only, zero-cost four-scene vertical video renderer. Requires Pillow, ffmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
SCENES=[("そのAI回答、","確認した？","最初の1秒で問いかける"),("BEFORE","AIの答えをコピペ","根拠がわからない"),("AFTER","出典・日付・数字","3点を確認する"),("最後は人が判断","確認してから使う","AIは補助、責任は人")]
def render(out: Path, font: str, bold: str):
    out.mkdir(parents=True,exist_ok=True)
    for i,(a,b,c) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),(8,18,35)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((64,160,1016,1750),radius=45,fill=(19,38,62),outline=(64,122,155),width=4)
        d.rectangle((64,160,80,1750),fill=(55,210,188))
        d.text((120,245),f"0{i+1} / 04",font=ImageFont.truetype(bold,42),fill=(88,220,199))
        d.text((115,520),a,font=ImageFont.truetype(bold,76),fill="white")
        d.text((115,740),b,font=ImageFont.truetype(bold,61),fill=(238,246,252))
        d.rounded_rectangle((115,1060,965,1300),radius=26,fill=(29,58,83))
        d.text((145,1140),c,font=ImageFont.truetype(font,40),fill=(205,229,241))
        d.rounded_rectangle((115,1520,115+int(850*(i+1)/4),1540),radius=8,fill=(66,220,191))
        d.text((115,1620),"REVIEW ONLY  •  NO AUDIO",font=ImageFont.truetype(font,30),fill=(152,177,194))
        im.save(out/f"frame{i}.png")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",str(out/f"frame{i}.png"),"-t","3","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",str(out/f"clip{i}.mp4")],check=True)
    (out/"concat.txt").write_text("".join(f"file '{(out/f'clip{i}.mp4').resolve()}'\n" for i in range(4)))
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(out/"concat.txt"),"-c","copy","-movflags","+faststart",str(out/"cycle1273_REVIEW_ONLY.mp4")],check=True)
    (out/"captions.srt").write_text("1\n00:00:00,000 --> 00:00:03,000\nそのAI回答、確認した？\n\n2\n00:00:03,000 --> 00:00:06,000\nBEFORE：AIの答えをコピペ\n\n3\n00:00:06,000 --> 00:00:09,000\nAFTER：出典・日付・数字を確認\n\n4\n00:00:09,000 --> 00:00:12,000\n最後は人が判断\n",encoding="utf8")
if __name__=="__main__":
    import sys
    render(Path(sys.argv[1]),sys.argv[2],sys.argv[3])
