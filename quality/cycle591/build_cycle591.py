"""cycle591: keyword-colored Japanese subtitles, no network or publishing."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets/cycle590.mp4"
OUT = ROOT / "output/cycle591_KEYWORD_CAPTIONS_HUMAN_REVIEW.mp4"
OVERLAY = ROOT / "assets/caption_overlay.mp4"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FPS, END_FRAME, CAPTION_Y, H = 30, 417, 1000, 215
SCENES = [
    {"start":0,"end":66,"lines":[("これ、","ただの","")]},
    {"start":66,"end":132,"lines":[("","ラズベリーパイ","ファイブ。")]},
    {"start":132,"end":216,"lines":[("","小さなパソコン","として、")]},
    {"start":216,"end":249,"lines":[("","プログラミング","や")]},
    {"start":249,"end":282,"lines":[("","電子工作","に使える。")]},
    {"start":282,"end":351,"lines":[("","自分だけ","の仕組みを")]},
    {"start":351,"end":417,"lines":[("作りたい人は、","",""),("","保存して","チェック。")]},
]

def hexrgb(h):
    return tuple(int(h.lstrip("#")[i:i+2],16) for i in (0,2,4))

def choose_font(parts, max_width=845, size=65):
    d = ImageDraw.Draw(Image.new("RGB",(1,1)))
    for sz in range(size,37,-1):
        font=ImageFont.truetype(FONT,sz)
        if sum(d.textlength(s,font=font) for s in parts)<=max_width:
            return font
    return ImageFont.truetype(FONT,38)

def make_caption(scene,theme="#39e6cc"):
    color=hexrgb(theme)
    im=Image.new("RGB",(1080,H),"#020d1b")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((54,17,1025,197),radius=25,fill="#0b2433",outline=color,width=3)
    d.rounded_rectangle((76,46,86,167),radius=5,fill=color)
    for (prefix,emphasis,suffix),y in zip(scene["lines"],[67] if len(scene["lines"])==1 else [30,105]):
        font=choose_font((prefix,emphasis,suffix))
        x=119
        d.text((x,y),prefix,font=font,fill="#f5fafc")
        pre=d.textlength(prefix,font=font)
        d.text((x+pre,y),emphasis,font=font,fill=color)
        w=d.textlength(emphasis,font=font)
        d.text((x+pre+w,y),suffix,font=font,fill="#f5fafc")
        ly=y+font.size+12
        if ly<195 and emphasis:
            d.rounded_rectangle((x+pre,ly,min(990,x+pre+w),ly+3),radius=1,fill=color)
    return im

def run(args):
    import cv2, numpy as np
    cfg=json.loads((ROOT/"config/genres.json").read_text(encoding="utf-8"))
    if args.genre not in cfg["genres"]:raise ValueError(args.genre)
    src,out=Path(args.source),Path(args.output)
    if not src.is_file():raise FileNotFoundError(src)
    out.parent.mkdir(parents=True,exist_ok=True)
    OVERLAY.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(OVERLAY),cv2.VideoWriter_fourcc(*"mp4v"),FPS,(1080,H))
    if not writer.isOpened():raise RuntimeError("Cannot create overlay")
    for scene in SCENES:
        arr=cv2.cvtColor(np.asarray(make_caption(scene,cfg["genres"][args.genre]["theme"])),cv2.COLOR_RGB2BGR)
        for _ in range(scene["end"]-scene["start"]):writer.write(arr)
    writer.release()
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-i",str(OVERLAY),
        "-filter_complex",f"[0:v][1:v]overlay=0:{CAPTION_Y}:enable=lt(n\\,{END_FRAME}):shortest=0:format=auto,format=yuv420p[v]",
        "-map","[v]","-map","0:a:0","-c:v","libx264","-preset","ultrafast","-threads","2",
        "-crf","19","-r","30","-frames:v","468","-pix_fmt","yuv420p","-c:a","copy",
        "-movflags","+faststart",str(out)],check=True)
    return out

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",default=str(SOURCE))
    p.add_argument("--output",default=str(OUT))
    p.add_argument("--genre",default="雑学・科学")
    print(run(p.parse_args()))
