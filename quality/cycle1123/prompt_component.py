"""Original 10-genre animated prompt-assembly illustration; no external media.
This is the reusable art component. Full 22.5s renderer and MP4 are supplied
separately for human review. It never sends prompts to an external AI.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

GENRES = ("ai_work","business","money","learning","health","lifestyle",
          "psychology","science","history","travel")
COLORS = ("#58E5D8","#71B8FF","#F6CA76","#A4A1FF","#6FE5B4",
          "#F5A5BF","#CE9CF6","#8FDDFB","#E4BA8C","#81D8D3")
PARTS = (("01","目的","週次報告を作る"),
         ("02","条件","数字と根拠を入れる"),
         ("03","形式","箇条書き3点"))
W,H=951,803
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def smooth(x):
    x=max(0.,min(1.,x))
    return x*x*(3-2*x)

def rgb(value):
    return tuple(int(value[i:i+2],16) for i in (1,3,5))

def font(size):
    if Path(FONT).exists():
        return ImageFont.truetype(FONT,size)
    return ImageFont.load_default()

def label(draw,xy,text,size,color):
    draw.text(xy,text,font=font(size),fill=color)

def rect(draw,coords,radius,fill,outline=None,width=1):
    draw.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)

def render_art(t,genre="ai_work"):
    """Draw only the safe illustration region, never the caption region."""
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    accent=rgb(COLORS[GENRES.index(genre)])
    im=Image.new("RGB",(W,H),(8,27,44))
    d=ImageDraw.Draw(im)
    rect(d,(0,0,W-1,H-1),34,(8,29,47),(51,99,117),3)
    glow=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(glow).ellipse((375,50,1010,690),fill=(*accent,65))
    im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(90))).convert("RGB")
    d=ImageDraw.Draw(im)
    rect(d,(30,25,440,89),18,(25,61,78),(63,121,135),2)
    label(d,(50,39),"3要素を組み立てる",30,accent)
    for i,(num,title,detail) in enumerate(PARTS):
        progress=smooth((t-(.10+i*.38))/.34)
        if progress<=0: continue
        y=150+i*175
        x=38-int(26*(1-progress))
        rect(d,(x+9,y+11,x+386,y+150),22,(2,13,25))
        rect(d,(x,y,x+377,y+139),22,(23,59,75),accent if progress>.85 else (49,95,108),3)
        rect(d,(x+17,y+20,x+91,y+87),16,(39,94,102))
        label(d,(x+28,y+34),num,29,accent)
        label(d,(x+108,y+20),title,37,(255,255,255))
        label(d,(x+29,y+95),detail,26,(199,230,235))
        if progress>.93:
            d.line((x+377,y+69,455,y+69),fill=accent,width=4)
            d.ellipse((446,y+61,463,y+78),fill=accent)
    rect(d,(470,137,922,696),28,(12,40,57),(69,135,149),3)
    rect(d,(486,154,905,216),15,(29,73,87))
    label(d,(505,168),"AIへの依頼文  /  例",27,(247,254,255))
    for i,line in enumerate(("目的：週次報告を作る","条件：数字と根拠を入れる","形式：箇条書き3点")):
        progress=smooth((t-(.30+i*.43))/.55)
        y=274+i*119
        rect(d,(491,y-13,901,y+82),13,(23,59,75))
        if progress>0:
            label(d,(510,y+8),line[:max(1,int(len(line)*progress))],27,(248,252,253))
    if smooth((t-1.78)/.55)>0:
        rect(d,(510,633,880,681),13,(34,103,103))
        label(d,(532,640),"具体的な指示が完成",25,(249,255,255))
    rect(d,(30,738,921,786),14,(20,52,68))
    label(d,(49,747),"目的 → 条件 → 形式  |  架空の入力例",27,(218,243,248))
    return im

if __name__=="__main__":
    import sys
    render_art(2.3,sys.argv[1] if len(sys.argv)>1 else "ai_work").save("prompt_preview.png")
