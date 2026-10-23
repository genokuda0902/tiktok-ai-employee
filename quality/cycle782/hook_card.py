"""Original animated hook card; portable 10-genre template (no stock assets)."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
WIDTH, HEIGHT, FRAMES = 1080, 1360, 57
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def load_genres(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))["genres"]
    if len(data)!=10 or len({x["name"] for x in data})!=10:
        raise ValueError("Expected 10 unique genres")
    for x in data:
        if len(x["accent"])!=7 or not x["accent"].startswith("#"):
            raise ValueError("Invalid accent")
    return data
def draw_frame(index=0, accent="#52EBD0", first="この基板、", second="実はパソコン。"):
    if not 0<=index<FRAMES: raise ValueError("Frame outside intro")
    t=index/(FRAMES-1)
    col=tuple(bytes.fromhex(accent.lstrip("#")))
    im=Image.new("RGB",(WIDTH,HEIGHT),(4,20,37))
    d=ImageDraw.Draw(im)
    f=lambda size:ImageFont.truetype(FONT,size)
    d.rounded_rectangle((60,45,345,120),radius=28,fill=(11,55,65),outline=col,width=3)
    d.text((200,82),"15秒でわかる",font=f(34),anchor="mm",fill="white")
    d.text((1000,82),"01 / 08",font=f(32),anchor="rm",fill=(180,204,210))
    d.line((60,145,1020,145),fill=(43,98,109),width=4)
    d.text((70,225),first,font=f(105),fill="white")
    d.text((70,355),second,font=f(105),fill=col)
    d.rounded_rectangle((60,580,1020,1230),radius=45,fill=(4,31,45),outline=(38,113,120),width=4)
    cx,cy=540+round(6*math.sin(t*math.pi)),885
    d.rounded_rectangle((cx-345,cy-215,cx+345,cy+215),radius=28,fill=(12,54,65),outline=col,width=7)
    for i in range(8):
        y=cy-160+i*45
        d.line((cx-280,y,cx-145,y),fill=(38,140,145),width=4)
        d.line((cx+145,y,cx+280,y),fill=(38,140,145),width=4)
    d.rounded_rectangle((cx-145,cy-125,cx+145,cy+125),radius=25,fill=(5,26,44),outline=(112,249,216),width=7)
    d.text((cx,cy),"CPU",font=f(74),anchor="mm",fill="white")
    scan_x=round(cx-300+600*t)
    d.line((scan_x,cy-180,scan_x,cy+180),fill=col,width=3)
    d.rounded_rectangle((310,1150,770,1215),radius=22,fill=(12,66,73),outline=col,width=2)
    d.text((540,1182),"手のひらサイズのコンピュータ",font=f(34),anchor="mm",fill="white")
    d.text((60,1320),"ORIGINAL ART / HUMAN REVIEW",font=f(20),fill=(140,175,184))
    return im
def export_frames(outdir,config,genre="雑学・科学"):
    genre_map={x["name"]:x for x in load_genres(config)}
    if genre!="雑学・科学":
        raise ValueError("Other genres need their own approved Japanese narration")
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for i in range(FRAMES):
        draw_frame(i,genre_map[genre]["accent"]).save(Path(outdir)/f"{i:03d}.png")
