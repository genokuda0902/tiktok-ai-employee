"""Review-only, original procedural kinetic hook (cycle501). Not original v33 code."""
from dataclasses import dataclass
from pathlib import Path
import argparse,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1080,1920,30
STAGES=(15,15,15,15,15)
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
@dataclass(frozen=True)
class Hook:
    genre:str="AI仕事効率化"
    values:tuple=(120,150,200,250)
    total:int=720
    asset_origin:str="original_procedural"
    synthetic:bool=True
    review_only:bool=True
    approved:bool=False
    auto_post:bool=False
    japanese_voice_verified:bool=False
def validate(s):
    if not (s.synthetic and s.asset_origin=="original_procedural" and s.review_only):
        raise ValueError("Unapproved source")
    if s.approved or s.auto_post or s.japanese_voice_verified:
        raise ValueError("False release/voice approval")
    if len(s.values)!=4 or any(type(x)!=int or x<0 for x in s.values):
        raise ValueError("Invalid values")
    if sum(s.values)!=s.total:raise ValueError("Invalid sum")
    if sum(STAGES)!=75:raise ValueError("Broken 2.5-second contract")
    return s.total
def draw(stage,s=Hook()):
    validate(s)
    if stage not in range(5):raise ValueError("Invalid stage")
    im=Image.new("RGB",(W,H),"#081e35");d=ImageDraw.Draw(im)
    def txt(x,y,v,n=50,c="white",bold=True):
        d.text((x,y),v,font=ImageFont.truetype(BOLD if bold else FONT,n),fill=c)
    def box(xy,color):
        d.rounded_rectangle(xy,radius=30,fill=color,outline="#4c9ac6",width=4)
    txt(55,80,"AI時短ラボ / ORIGINAL SYNTHETIC DEMO",30,"#6bdfff")
    box((55,185,1025,440),"#15354e")
    txt(95,225,"まだ手で合計？" if stage==0 else "4つの数字を検算",85,"#ffe17b")
    # Distinct original robot face, no third-party media or marks
    d.ellipse((340,555,740,990),fill="#0c4061",outline="#4ad9ff",width=10)
    d.rounded_rectangle((366,606,713,918),radius=120,fill="#071a30",outline="#a2f3ff",width=6)
    for x in (445,620):
        d.ellipse((x-35,715,x+35,785),fill="#4ad9ff")
        d.ellipse((x-14,735,x+14,763),fill="#ffffff")
    d.arc((480,780,605,865),start=20,end=160,fill="#5ceadf",width=8)
    box((55,1090,1025,1535),"#123652")
    txt(100,1130,"架空の売上データ / 4か月",45,"#c9edfa")
    for i,v in enumerate(s.values):
        x=95+i*234
        shown=(stage>=3 or i<max(1,stage))
        box((x,1240,x+195,1385),"#1c5975" if shown else "#183448")
        txt(x+22,1274,str(v) if shown else "···",49)
    txt(90,1445,"120+150+200+250 = 720" if stage>=3 else "数字を確認中…",43,"#7cf3d7")
    box((55,1570,1025,1740),"#0c615c")
    txt(98,1610,"このあと操作を実演" if stage==4 else "SUM関数で根拠を確認",52)
    txt(55,1790,"再現映像 / 架空データ / 投稿未承認",29,"#b2cddb")
    d.line((60,1860,1020,1860),fill="#285473",width=10)
    d.line((60,1860,60+int(960*(stage+1)/5),1860),fill="#55e6da",width=10)
    return im
def render(out):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        t=Path(td);clips=[]
        for i,n in enumerate(STAGES):
            png=t/f"{i}.png";draw(i).save(png)
            clip=t/f"{i}.mp4";clips.append(clip)
            subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-loop","1","-framerate","30","-i",str(png),"-frames:v",str(n),"-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-an",str(clip)],check=True)
        listing=t/"list.txt";listing.write_text("".join(f"file '{p}'\n" for p in clips))
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy",str(out)],check=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    render(p.parse_args().out)
