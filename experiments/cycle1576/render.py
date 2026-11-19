"""Review-only vertical caption animation. Reimplementation, not v33."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES = [("AIで仕事を速くする","まず、作業を分解する"),("入力を減らす","テンプレートを作る"),("確認を残す","最後は人がチェック"),("今日から1つ試す","小さく始めて改善")]
WIDTH, HEIGHT, FPS, DURATION = 720, 1280, 24, 8

def render(output, font_path="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    font = lambda size: ImageFont.truetype(font_path,size)
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{WIDTH}x{HEIGHT}","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):
        t=i/FPS; scene=min(3,int(t//2)); title,subtitle=SCENES[scene]
        im=Image.new("RGB",(WIDTH,HEIGHT),(9,17,33)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((35,115,685,1125),radius=36,fill=(21,35,58))
        d.text((70,205),f"AI WORKFLOW / {scene+1}",font=font(27),fill=(100,219,231))
        d.text((70,325),title,font=font(43),fill="white")
        d.text((70,435),subtitle,font=font(32),fill=(210,222,234))
        progress=min(1,max(0,((t%2)-.2)/1.3))
        for j in range(3):
            y=600+j*105
            d.rounded_rectangle((90,y,625,y+48),radius=14,fill=(41,58,81))
            d.rounded_rectangle((90,y,90+int((170+j*125)*progress),y+48),radius=14,fill=(35,182,205))
        d.text((70,1020),"REVIEW ONLY / 投稿不可",font=font(24),fill=(244,181,103))
        d.rectangle((70,1160,70+int(580*(i+1)/(FPS*DURATION)),1170),fill=(45,204,221))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait()!=0: raise RuntimeError("ffmpeg render failed")

if __name__=="__main__":
    render(Path("cycle1576_REVIEW_ONLY.mp4"))
