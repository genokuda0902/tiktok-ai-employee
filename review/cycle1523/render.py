"""Review-only synthetic spreadsheet demo. No third-party assets, no narration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
W,H,FPS,DURATION=720,1280,24,8
STEPS=[(0,2,"合計を手計算していませんか？","3つの数字を一瞬で集計"),(2,4,"セルに数式を入力","=SUM(B2:B4)"),(4,6,"Enterで結果が出る","120 + 250 + 330 = 700"),(6,8,"同じ作業を短縮","まずはSUM関数から")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def scene(t):
    return next((i for i,(a,b,_,__) in enumerate(STEPS) if a<=t<b),len(STEPS)-1)
def draw(t):
    im=Image.new("RGB",(W,H),"#0a1222"); d=ImageDraw.Draw(im)
    title=ImageFont.truetype(BOLD,42); body=ImageFont.truetype(FONT,30); small=ImageFont.truetype(FONT,23); digit=ImageFont.truetype(BOLD,35)
    d.rounded_rectangle((36,68,684,170),radius=24,fill="#14263c")
    d.text((60,91),"1分でわかる Excel時短",font=title,fill="#ffffff")
    idx=scene(t); a,b,headline,detail=STEPS[idx]
    d.text((42,225),headline,font=title,fill="#ffffff")
    d.text((44,296),detail,font=body,fill="#80e8dd")
    d.rounded_rectangle((40,405,680,955),radius=20,fill="#f4f7fa")
    d.rectangle((40,405,680,467),fill="#08765c")
    d.text((65,419),"売上集計  /  サンプル",font=body,fill="white")
    for row in range(5):
        y=480+row*83
        d.line((64,y+75,654,y+75),fill="#d4dce5",width=2)
        d.text((78,y+16),["項目","A商品","B商品","C商品","合計"][row],font=body,fill="#243448")
        if row in (1,2,3): d.text((490,y+16),["","120","250","330"][row],font=digit,fill="#243448")
    if idx>=1:
        d.rounded_rectangle((375,805,645,883),radius=9,fill="#d7f5ed",outline="#0c9576",width=3)
        d.text((389,822),"=SUM(B2:B4)" if idx==1 else "700",font=body,fill="#074b3d")
    d.text((46,1030),"操作 → 結果 → 活用",font=body,fill="#e7effa")
    d.rounded_rectangle((42,1100,678,1113),radius=6,fill="#31415b")
    d.rounded_rectangle((42,1100,42+int(636*t/DURATION),1113),radius=6,fill="#44ddbf")
    d.text((44,1160),"REVIEW ONLY / 音声未生成・投稿不可",font=small,fill="#f3bb79")
    return im
def render():
    out=ROOT/"cycle1523_REVIEW_ONLY.mp4"
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(FPS*DURATION): p.stdin.write(draw(n/FPS).tobytes())
    p.stdin.close()
    if p.wait(): raise RuntimeError("ffmpeg failed")
    return out
if __name__=="__main__": print(render())
