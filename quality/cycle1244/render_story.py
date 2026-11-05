"""Review-only synthetic storyboard. Pillow + ffmpeg required; no voice claims."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, argparse
W,H=720,1280
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def frame(t):
    im=Image.new("RGB",(W,H),(10,17,33)); d=ImageDraw.Draw(im)
    f=lambda n:ImageFont.truetype(FONT,n)
    stage=0 if t<4 else 1 if t<9 else 2
    d.rounded_rectangle((36,70,684,1200),radius=32,fill=(22,34,55))
    d.text((62,120),"AI × 仕事術",font=f(34),fill="#5EEAD4")
    d.text((62,205),"架空データの集計デモ",font=f(36),fill="white")
    d.text((62,340),["BEFORE","ACTION","AFTER"][stage],font=f(36),fill="#5EEAD4")
    for i,(label,value) in enumerate([("A","120"),("B","180"),("C","200"),("合計",["未計算","=SUM(B2:B4)","500"][stage])]):
        y=455+i*105
        d.rounded_rectangle((65,y,655,y+85),radius=12,outline="#64748B",width=2)
        d.text((90,y+17),label,font=f(30),fill="white")
        d.text((365,y+17),value,font=f(28),fill="#FDE68A")
    d.text((62,980),["手作業で合計を確認","SUM関数を入力","合計500を確認"][stage],font=f(29),fill="white")
    d.text((62,1120),"REVIEW ONLY / 公開未承認",font=f(22),fill="#FDA4AF")
    d.rectangle((62,1080,62+int(596*min(t/15,1)),1090),fill="#5EEAD4")
    return im
def render(output):
    cmd=["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s","720x1280","-r","12","-i","-","-an","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(180): p.stdin.write(frame(i/12).tobytes())
    p.stdin.close()
    if p.wait(): raise RuntimeError("ffmpeg render failed")
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("output",type=Path);render(parser.parse_args().output)
