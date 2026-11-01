"""Cycle1159: animated fictional spreadsheet-style example, for human review only.

The example is calculated from explicit fictional data. It is NOT a genuine
Excel screenshot and does NOT certify narration/subtitle alignment or rights.
"""
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,X,Y=920,630,80,540
START_FRAME=168
FRAMES=82
FPS=30
DATA=((1,12,9),(2,18,14),(3,24,21))
PALETTES={
    "ai-work":"#32c6b7","finance":"#d7b55e","career":"#6dcca5",
    "health":"#72c7b7","learning":"#72b5ef","travel":"#e8a66d",
    "technology":"#79b5ed","business":"#43bfc0","life":"#dd9bc5",
    "history":"#d0a775"
}
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def stats(rows=DATA):
    if not rows or any(len(r)!=3 or min(r)<0 or r[2]>r[1] for r in rows):
        raise ValueError("Invalid fictional rows")
    total=sum(r[1] for r in rows)
    done=sum(r[2] for r in rows)
    return {"total":total,"done":done,"remaining":total-done,
            "rate":round(100*done/total,1) if total else 0.0}

def safe(x=X,y=Y,w=W,h=H):
    if min(x,y)<0 or min(w,h)<=0 or x+w>1080 or y+h>1240:
        raise ValueError("Would cover title, narration, or leave frame")
    return True

def ft(n,b=False):
    return ImageFont.truetype(BOLD if b else REG,n)

def rounded(d,box,color,r=8,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=color,outline=outline,width=width)

def frame(i,genre="ai-work"):
    if genre not in PALETTES or not 0<=i<FRAMES:
        raise ValueError("Unknown genre or frame")
    safe()
    t=i/FPS
    accent=PALETTES[genre]
    s=stats()
    im=Image.new("RGBA",(W,H),(5,17,29,255))
    d=ImageDraw.Draw(im)
    rounded(d,(4,4,W-5,H-5),"#0c2334",20,"#397b80",3)
    rounded(d,(18,18,W-18,80),"#143b43",12)
    rounded(d,(34,30,75,68),"#238765",7)
    d.text((45,32),"X",font=ft(26,True),fill="white")
    d.text((90,29),"週次集計_デモ",font=ft(26,True),fill="#f2fafb")
    d.text((92,62),"SPREADSHEET PREVIEW",font=ft(13),fill="#9ebfca")
    rounded(d,(650,30,883,66),"#27414d",12)
    d.text((668,35),"架空データ・操作イメージ",font=ft(17,True),fill="#c9f3e9")
    d.text((34,92),"ホーム     挿入     数式     データ",font=ft(18),fill="#d7e6eb")
    rounded(d,(24,130,896,183),"#f3f7f9")
    d.text((42,138),"fx",font=ft(22,True),fill="#168268")
    d.line((85,140,85,174),fill="#b6cbd0",width=2)
    d.text((104,139),"=SUM(C2:C4)" if t<1.75 else "=SUM(B2:B4)",
           font=ft(23),fill="#19323a")
    rounded(d,(24,195,896,507),"#f9fbfd",5)
    xs=[55,270,465,659,895]
    ys=[225,273,326,379,432,496]
    d.rectangle((24,195,895,225),fill="#dce8eb")
    d.text((35,196),"#",font=ft(15,True),fill="#58717b")
    for col,label in enumerate("ABCD"):
        d.text((xs[col]+24,196),label,font=ft(17,True),fill="#51666f")
    d.rectangle((55,225,895,273),fill="#e8f4f0")
    for c,label in enumerate(("週","案件","完了","未完了")):
        d.text((xs[c]+22,231),label,font=ft(20,True),fill="#26454d")
    for row,(week,requests,done) in enumerate(DATA):
        y=ys[row+1]
        if row%2==0:d.rectangle((55,y,895,ys[row+2]),fill="#f0f6f8")
        for c,value in enumerate((f"{week}週",requests,done,requests-done)):
            d.text((xs[c]+22,y+9),str(value),font=ft(22,True),fill="#2d4953")
    d.rectangle((55,432,895,496),fill="#e1f4ef")
    for c,value in enumerate(("合計",s["total"],s["done"],s["remaining"])):
        d.text((xs[c]+22,445),str(value),font=ft(25,True),fill="#1b5149")
    for x in xs:d.line((x,195,x,507),fill="#d1dfe4",width=2)
    for y in ys:d.line((24,y,896,y),fill="#d1dfe4",width=2)
    for r in range(1,6):
        d.text((33,ys[r-1]+11),str(r),font=ft(15),fill="#5d737b")
    if t<1.70:
        progress=max(0,min(1,(t-.42)/.45))
        bottom=int(273+progress*(432-273))
        d.rectangle((465,273,659,bottom),fill=(56,198,174,48),outline=accent,width=5)
        d.ellipse((648,bottom-10,666,bottom+8),fill=accent)
    else:
        d.rectangle((270,432,465,496),outline=accent,width=5)
    rounded(d,(24,521,896,608),"#0e3440",12,"#3c6c72",2)
    d.text((45,536),"3週間の集計",font=ft(20,True),fill="#cce8e8")
    if t<1.72:
        d.text((250,536),"対象セルを選択中…",font=ft(24,True),fill="#c8dfe5")
        d.text((250,574),"※ 表示値はすべて架空の例です",font=ft(15),fill="#a3bec5")
    else:
        progress=max(0,min(1,(t-1.72)/.55))
        d.text((252,532),f"案件 {s['total']}件",font=ft(24,True),fill="white")
        d.text((490,532),f"完了 {s['done']}件",font=ft(24,True),fill="white")
        d.text((726,532),f"{s['rate']:.1f}%",font=ft(25,True),fill=accent)
        rounded(d,(251,581,853,590),"#30535e",4)
        rounded(d,(251,581,251+int(602*s["rate"]/100*progress),590),accent,4)
    return im

def run(cmd):
    return subprocess.run(cmd,check=True,capture_output=True).stdout

def render(source,output,overlay,genre="ai-work"):
    source,output,overlay=map(Path,(source,output,overlay))
    if genre not in PALETTES:raise ValueError("Unknown genre")
    info=json.loads(run(["ffprobe","-v","error","-show_streams","-of","json",str(source)]))
    v=next(s for s in info["streams"] if s["codec_type"]=="video")
    if (v["width"],v["height"],v["avg_frame_rate"])!=(1080,1920,"30/1"):
        raise ValueError("1080x1920 30fps required")
    if not any(s["codec_type"]=="audio" for s in info["streams"]):
        raise ValueError("Existing Japanese narration audio required")
    overlay.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba",
         "-s",f"{W}x{H}","-r","30","-i","pipe:0","-c:v","qtrle",
         "-pix_fmt","argb",str(overlay)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):proc.stdin.write(frame(i,genre).tobytes())
        proc.stdin.close()
        err=proc.stderr.read()
        if proc.wait()!=0:raise RuntimeError(err.decode(errors="replace"))
    finally:
        if proc.poll() is None:proc.kill();proc.wait()
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=(f"[1:v]setpts=PTS+{START_FRAME/FPS}/TB[ov];"
          f"[0:v][ov]overlay={X}:{Y}:eof_action=pass:format=auto,"
          "format=yuv420p[v]")
    run(["ffmpeg","-v","error","-y","-i",str(source),"-i",str(overlay),
         "-filter_complex",filt,"-map","[v]","-map","0:a:0",
         "-c:v","libx264","-preset","veryfast","-crf","18",
         "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)])
    return {"output":str(output),"scene":3,"start_frame":START_FRAME,
            "frames":FRAMES,"genres":len(PALETTES),"fictional":True,
            "audio_copied":True,"publication_approved":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--overlay",required=True)
    p.add_argument("--genre",choices=PALETTES,default="ai-work")
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.overlay,a.genre),ensure_ascii=False))
