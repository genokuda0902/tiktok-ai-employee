#!/usr/bin/env python3
"""Synthetic evidence subtotal animation. REVIEW_ONLY; no narration or posting."""
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NUM=(120,150,200,250)
LAB=("1月","2月","3月","4月")

def validate(nums,labels,claimed):
    if not nums or len(nums)!=len(labels) or len(nums)>8:
        raise ValueError("missing or mismatched inputs")
    if any(type(x) is not int or x<0 for x in nums):
        raise ValueError("nonnegative integers only")
    if any(not isinstance(x,str) or not x.strip() for x in labels):
        raise ValueError("missing label")
    if sum(nums)!=claimed:
        raise ValueError("untrue result")
    return True

def stage(t,n):
    return min(n,max(1,int(t/.45)+1))

def render(t,nums=NUM,labels=LAB):
    validate(nums,labels,sum(nums))
    n=stage(t,len(nums)); complete=n==len(nums)
    im=Image.new("RGB",(W,H),"#061628")
    d=ImageDraw.Draw(im,"RGBA")
    def f(sz):return ImageFont.truetype(FONT,sz)
    for y in range(0,H,12):
        d.rectangle((0,y,W,y+12),fill=(6,22+int(12*y/H),40+int(14*y/H),255))
    d.rounded_rectangle((72,188,1008,300),radius=22,fill=(7,98,111,255))
    d.text((110,209),"EVIDENCE / VERIFY",font=f(46),fill="white")
    d.text((74,354),"元データを、順番に検算。",font=f(59),fill="white")
    d.text((76,449),"途中経過と確定結果を区別する",font=f(33),fill="#92e5df")
    for i,(label,value) in enumerate(zip(labels,nums)):
        x=72+(i%2)*478; y=610+(i//2)*248; active=i<n
        d.rounded_rectangle((x,y,x+452,y+219),radius=24,
          fill=(11,76,91,255) if active else (22,41,58,255),
          outline=(42,223,216,255) if active else (65,89,108,255),width=4)
        d.text((x+34,y+26),label,font=f(40),fill="#c2e6ea")
        d.text((x+34,y+90),str(value),font=f(78),
               fill="white" if active else "#768b99")
        if active:d.ellipse((x+390,y+33,x+416,y+59),fill="#43eeda")
    d.rounded_rectangle((72,1155,1008,1506),radius=32,
      fill=(7,53,69,255),outline=(31,191,190,255),width=4)
    d.text((110,1195),"検算OK / 合計" if complete else "途中経過 / 計算中",
           font=f(47),fill="#83f5e1")
    d.text((110,1290),str(sum(nums[:n])),font=f(113),fill="white")
    d.text((110,1442)," + ".join(map(str,nums[:n])),font=f(29),fill="#cae6eb")
    d.rounded_rectangle((72,1545,1008,1593),radius=18,fill="#143447")
    d.rounded_rectangle((72,1545,72+int(936*n/len(nums)),1593),
                        radius=18,fill="#23d7c3")
    d.text((76,1650),"※ 架空データによる再現・実績値ではありません",
           font=f(27),fill="#acbfcb")
    d.text((76,1714),"HUMAN REVIEW / PUBLICATION NOT APPROVED",
           font=f(22),fill="#92a6b1")
    return im

def make(base,output):
    base=Path(base);output=Path(output)
    if not base.is_file():raise FileNotFoundError(base)
    output.parent.mkdir(parents=True,exist_ok=True)
    segment=output.parent/"cycle551_segment.mp4"
    enc=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24",
         "-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-an","-c:v",
         "libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p",str(segment)]
    p=subprocess.Popen(enc,stdin=subprocess.PIPE)
    try:
        for i in range(78):p.stdin.write(render(i/FPS).tobytes())
        p.stdin.close()
        if p.wait()!=0:raise RuntimeError("segment encode failed")
    finally:
        if p.poll() is None:p.kill()
    fc=("[1:v]setpts=PTS-STARTPTS+16/TB[ov];"
        "[0:v][ov]overlay=0:0:eof_action=pass:shortest=1:"
        "enable='gte(t,16)*lt(t,18.6)',format=yuv420p[v]")
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(base),"-i",str(segment),
      "-filter_complex",fc,"-map","[v]","-map","0:a:0","-frames:v","600",
      "-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p",
      "-c:a","copy","-movflags","+faststart",str(output)],check=True)
    return output

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    print(make(args.base,args.output))
