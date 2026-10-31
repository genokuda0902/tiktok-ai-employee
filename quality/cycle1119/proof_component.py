"""cycle1119: original proof-first vertical image-slide component (review only).

No customer data, no web assets, no posting. The full private 22.5s
renderer and Japanese MP4 are distributed separately in the review ZIP.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W,H,FPS=1080,1920,30
GENRES=("ai_work","business","money","learning","health","lifestyle",
        "psychology","science","history","travel")
PALETTES=("#58E5D8","#71B8FF","#F6CA76","#A4A1FF","#6FE5B4",
          "#F5A5BF","#CE9CF6","#8FDDFB","#E4BA8C","#81D8D3")
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def _font(size,bold=False):
    path=BOLD if bold else FONT
    if Path(path).exists(): return ImageFont.truetype(path,size)
    return ImageFont.load_default()

def _color(hexval):
    return tuple(int(hexval[i:i+2],16) for i in (1,3,5))

def smoothstep(x):
    x=max(0.,min(1.,x))
    return x*x*(3-2*x)

def _text(d,xy,s,size,color,bold=False):
    d.text(xy,s,font=_font(size,bold),fill=color)

def _panel(d,rect,fill,outline):
    d.rounded_rectangle(rect,radius=24,fill=fill,outline=outline,width=3)

def draw_hook_frame(t,genre="ai_work"):
    """Frame from original 1.5s question hook; fictional data is explicit."""
    if genre not in GENRES: raise ValueError("Unknown genre")
    accent=_color(PALETTES[GENRES.index(genre)])
    im=Image.new("RGB",(W,H),(5,23,39));d=ImageDraw.Draw(im)
    _text(d,(80,130),"AI時短ラボ  /  DEMO",32,accent,True)
    _text(d,(80,250),"その集計、",87,"white",True)
    _text(d,(80,365),"まだ手作業？",91,(255,222,136),True)
    _panel(d,(76,570,515,1190),(13,44,63),(51,111,128))
    _panel(d,(550,570,1006,1190),(13,44,63),accent)
    _text(d,(96,605),"手作業の集計例",33,"white",True)
    _text(d,(570,605),"整理後の表示例",33,"white",True)
    for i,(week,count,done) in enumerate((("1週","12","9"),("2週","18","14"),("3週","24","21"))):
        y=745+i*110
        _text(d,(102,y),week,30,accent,True)
        _text(d,(240,y),count,30,"white",True)
        _text(d,(375,y),done,30,"white",True)
    d.line((600,1050,975,1050),fill=(90,135,151),width=3)
    for i,val in enumerate((12,18,24)):
        rise=int(290*val/24*smoothstep((t-.18)/.86))
        if rise: d.rounded_rectangle((620+i*120,1050-rise,695+i*120,1050),radius=10,fill=accent)
    _text(d,(99,1125),"※ 架空の数値",24,(167,204,218))
    _text(d,(92,1270),"完成形を見せると、伝わりやすい。",34,"white",True)
    _panel(d,(68,1365,872,1648),(4,21,38),(44,127,129))
    _text(d,(123,1405),"ナレーション",26,accent,True)
    _text(d,(123,1465),"AIで仕事を速くするなら、",47,"white",True)
    _text(d,(95,1800),"確認用サンプル・社員承認前・投稿禁止",23,(158,192,208))
    return im

def draw_proof_frame(t,genre="ai_work"):
    """Fictional spreadsheet-to-chart proof. Never draw over captions y>=1365."""
    if genre not in GENRES: raise ValueError("Unknown genre")
    accent=_color(PALETTES[GENRES.index(genre)])
    im=Image.new("RGB",(W,H),(7,26,43));d=ImageDraw.Draw(im)
    _text(d,(85,235),"完成形を先に見せる",70,"white",True)
    _text(d,(85,338),"見本があると、指示が伝わる",34,(187,221,231))
    _panel(d,(72,510,1007,1306),(9,31,49),(43,99,116))
    _text(d,(102,545),"見本：週次報告（架空）",31,accent,True)
    _panel(d,(92,635,522,1165),(15,47,65),(57,104,119))
    _panel(d,(552,635,987,1165),(15,47,65),accent)
    _text(d,(117,665),"元データ",31,"white",True)
    _text(d,(580,665),"完成イメージ",31,"white",True)
    for i,(week,num) in enumerate((("1週",12),("2週",18),("3週",24))):
        y=785+i*99
        _text(d,(119,y),week,32,"white",True)
        _text(d,(316,y),str(num),32,accent,True)
        bh=int(245*num/24*smoothstep((t-.55)/1.05))
        if bh:d.rounded_rectangle((608+i*117,1057-bh,680+i*117,1057),radius=9,fill=accent)
    _text(d,(116,1090),"※ 架空の数値",24,(165,204,218))
    _text(d,(102,1225),"先に完成例を示すと、指示が具体的になる。",28,"white",True)
    return im
