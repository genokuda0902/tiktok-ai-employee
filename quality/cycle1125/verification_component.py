"""Original 3-beat verification scan artwork; fictional figures only.
Only renders review illustration. Never fact-checks real data or posts.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=951,803
GENRES=("ai_work","business","money","learning","health","lifestyle","psychology","science","history","travel")
ACCENTS=("#58E5D8","#71B8FF","#F6CA76","#A4A1FF","#6FE5B4","#F5A5BF","#CE9CF6","#8FDDFB","#E4BA8C","#81D8D3")
CHECKS=(("数字","元データと照合","成約 24件"),("日付","対象期間を確認","10月31日"),("断定","根拠と表現を確認","必ず改善"))
BEATS=(.17,.95,1.72)
def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def mix(a,b,t):return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
def font(n,bold=False):
    p='/usr/share/fonts/opentype/noto/NotoSansCJK-'+('Bold' if bold else 'Regular')+'.ttc'
    return ImageFont.truetype(p,n)
def text(d,xy,s,n,c,b=False):d.text(xy,s,font=font(n,b),fill=c)
def rr(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def render_art(t,genre="ai_work"):
    if genre not in GENRES:raise ValueError("unsupported genre")
    accent=rgb(ACCENTS[GENRES.index(genre)]);white=(241,252,255)
    im=Image.new("RGB",(W,H),(8,27,44));d=ImageDraw.Draw(im)
    rr(d,(0,0,950,802),34,(8,29,47),(54,104,120),3)
    glow=Image.new("RGBA",(W,H),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((350,-70,1020,600),fill=(*accent,55))
    im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(85))).convert("RGB");d=ImageDraw.Draw(im)
    rr(d,(29,26,469,89),17,(24,61,78),(55,112,130),2)
    text(d,(49,38),"回答を使う前に確認",30,accent,True)
    text(d,(777,45),"確認 / 3項目",22,(176,211,222),True)
    rr(d,(43,157,452,675),25,(3,17,31))
    rr(d,(35,147,444,665),25,(21,54,70),(71,124,143),3)
    rr(d,(53,167,425,230),14,(38,85,101))
    text(d,(70,179),"AIの出力例（架空）",27,white,True)
    for i,(key,detail,value) in enumerate(CHECKS):
        y=270+i*122
        rr(d,(56,y,422,y+100),13,(27,65,82))
        text(d,(74,y+12),key,22,(172,204,217),True)
        text(d,(74,y+43),value,32,white,True)
        progress=smooth((t-BEATS[i])/.4)
        if progress:
            rr(d,(55,y+2,61,y+98),3,accent)
            if progress<1:
                x=70+int(320*progress);d.line((x,y+6,x,y+93),fill=accent,width=4)
    for i,(key,detail,value) in enumerate(CHECKS):
        y=158+i*163;p=smooth((t-BEATS[i])/.45)
        rr(d,(487,y+9,926,y+145),20,(3,17,31))
        rr(d,(479,y,918,y+136),20,mix((17,46,63),(30,80,91),p),mix((48,91,107),accent,p),3)
        rr(d,(496,y+22,565,y+89),17,mix((30,69,83),accent,p*.84))
        text(d,(509,y+37),f"{i+1:02}",27,mix((180,210,218),(9,29,42),p),True)
        text(d,(586,y+14),key,35,white,True)
        text(d,(586,y+73),detail,27,mix((169,206,216),white,p),True)
        if p>.95:d.ellipse((886,y+20,903,y+37),fill=accent)
        if p>.08:d.line((443,y+67,478,y+67),fill=accent,width=3)
    rr(d,(36,715,918,784),15,(20,54,70))
    text(d,(57,732),"数字・日付・断定を、人が確認してから使う",28,white,True)
    return im
