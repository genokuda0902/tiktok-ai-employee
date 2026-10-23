#!/usr/bin/env python3
"""Zero-purchase Japanese Open JTalk narration CI sample.
Creates 8 original graphic slides, 8 narrated clips and one 1080x1920 MP4.
Technical sample only: not human-reviewed and not an assertion of voice quality.
"""
import json, os, subprocess, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).parent
OUT=ROOT/"out"
OUT.mkdir(parents=True,exist_ok=True)
TEXTS=[
 "この基板、実はパソコン。",
 "手のひらサイズ、でも本格派。",
 "画面につなげば、操作できる。",
 "必要なのは、三つの接続。",
 "LEDも光らせられる。",
 "入力、処理、出力。",
 "最初は、たった一行。",
 "保存して、あとで試そう。"
]
TITLES=["基板の正体","小さくても本格派","画面へ接続","3つの接続","LEDの実験","コンピューターの基本","Pythonの第一歩","保存して試そう"]
PALETTE={
"ai_work":"#B9A4FF","beauty":"#FFB9DF","love_psychology":"#D7B5FF",
"money_saving":"#89EFCB","sales_business":"#7FD7FF","career":"#A4D8FF",
"health_life":"#8AF0D1","science":"#43E5D0","travel_food":"#87E1F2",
"product_life":"#D4B6FF"
}
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def run(*args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)
def voice_config():
    voices=list(Path("/usr/share").rglob("*.htsvoice"))
    dics=list(Path("/var/lib/mecab/dic").rglob("naist-jdic"))
    if not voices or not dics:
        raise RuntimeError("Open JTalk Japanese voice or dictionary missing")
    return str(dics[0]),str(voices[0])
def slide(i):
    im=Image.new("RGB",(1080,1920),"#071C2E")
    d=ImageDraw.Draw(im)
    ac=PALETTE["science"]
    f1=ImageFont.truetype(FONT,77)
    f2=ImageFont.truetype(FONT,69)
    f3=ImageFont.truetype(FONT,42)
    d.rounded_rectangle((70,90,1010,195),radius=28,fill="#12394C",outline=ac,width=5)
    d.text((115,104),"TECH  /  QUICK LEARN",font=f3,fill=ac)
    d.text((840,112),f"{i+1:02d}/08",font=f3,fill="white")
    d.rounded_rectangle((75,325,1005,1370),radius=42,fill="#10364A",outline="#397E8C",width=5)
    d.text((125,405),TITLES[i],font=f1,fill="white")
    # Purely original abstract illustration; never claim it depicts actual hardware.
    for j in range(7):
        x=200+j*106
        d.rounded_rectangle((x,690+(j%2)*100,x+70,920+(j%2)*100),radius=15,fill="#0C7280",outline=ac,width=5)
        d.ellipse((x+20,810+(j%2)*100,x+50,840+(j%2)*100),fill="#F7C86A")
    d.rounded_rectangle((75,1470,1005,1720),radius=32,fill="#061521",outline="#4B8A98",width=4)
    s=TEXTS[i]
    sz=65
    while d.textbbox((0,0),s,font=ImageFont.truetype(FONT,sz))[2]>845:sz-=3
    d.text((105,1530),s,font=ImageFont.truetype(FONT,sz),fill="#FFFFFF")
    d.text((90,1800),"INTERNAL HUMAN REVIEW  •  NO AUTO-POST",font=ImageFont.truetype(FONT,25),fill="#96B7C0")
    p=OUT/f"slide_{i:02d}.png";im.save(p)
    return p
def main():
    dic,model=voice_config()
    segments=[]
    for i,s in enumerate(TEXTS):
        raw=OUT/f"speech_{i:02d}.wav"
        proc=subprocess.run(["open_jtalk","-x",dic,"-m",model,"-r","1.12","-ow",str(raw)],input=s.encode("utf-8"),check=True)
        with wave.open(str(raw),"rb") as w:
            dur=w.getnframes()/w.getframerate()
        if dur<0.25 or dur>12:raise RuntimeError(f"bad voice segment {i}: {dur}")
        image=slide(i)
        clip=OUT/f"part_{i:02d}.mp4"
        run("ffmpeg","-hide_banner","-loglevel","error","-y",
            "-loop","1","-framerate","30","-i",str(image),"-i",str(raw),
            "-t",str(dur),"-r","30","-c:v","libx264","-preset","ultrafast",
            "-pix_fmt","yuv420p","-c:a","aac","-ar","48000",
            "-movflags","+faststart",str(clip))
        segments.append((clip,dur))
    manifest=OUT/"concat.txt"
    manifest.write_text("".join("file '"+str(p.resolve())+"'\n" for p,_ in segments))
    final=OUT/"cycle802_NEW_JAPANESE_TTS_TECHNICAL_HUMAN_REVIEW.mp4"
    run("ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0",
        "-i",str(manifest),"-c","copy","-movflags","+faststart",str(final))
    run("ffmpeg","-v","error","-xerror","-i",str(final),"-f","null","-")
    meta={"voice_engine":"Open JTalk (free, local to GitHub Actions)","voice_model":Path(model).name,
          "segments":[{"text":t,"seconds":round(d,3)} for t,(_,d) in zip(TEXTS,segments)],
          "rights":"Original CI illustrations; verify Open JTalk voice/model licenses before publication",
          "status":"HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"}
    (OUT/"voice_qa.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print("Generated",final,"seconds",round(sum(x[1] for x in segments),2))
if __name__=="__main__":main()
