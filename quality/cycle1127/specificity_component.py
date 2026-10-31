"""Original animated Japanese before/after editing illustration. No external assets, personal data, or posting."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=951,803
GENRES=('ai_work','business','money','learning','health','lifestyle','psychology','science','history','travel')
ACCENTS=('#58E5D8','#71B8FF','#F6CA76','#A4A1FF','#6FE5B4','#F5A5BF','#CE9CF6','#8FDDFB','#E4BA8C','#81D8D3')
BEATS=(.30,.70,1.50,2.14)
VAGUE='もっと良くして'
SPECIFIC='見出しを短くして'
def font(n,bold=False):
    return ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-'+('Bold' if bold else 'Regular')+'.ttc',n)
def text(d,xy,s,n,c,b=False): d.text(xy,s,font=font(n,b),fill=c)
def rgb(s): return tuple(int(s[i:i+2],16) for i in (1,3,5))
def mix(a,b,f): return tuple(round(a[i]*(1-f)+b[i]*f) for i in range(3))
def smooth(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)
def rr(d,box,r,fill,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def visible_chars(t):
    return max(0,min(len(SPECIFIC),int((t-BEATS[1])/1.10*len(SPECIFIC)+.0001)))
def render_art(t,genre='ai_work'):
    if genre not in GENRES: raise ValueError('unsupported genre')
    accent=rgb(ACCENTS[GENRES.index(genre)]);white=(245,252,255)
    im=Image.new('RGB',(W,H),(7,26,43));d=ImageDraw.Draw(im)
    rr(d,(1,1,W-2,H-2),33,(9,29,47),(49,96,111),3)
    glow=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(glow)
    gd.ellipse((340,-140,1120,650),fill=(*accent,60))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(88))).convert('RGB');d=ImageDraw.Draw(im)
    rr(d,(31,27,467,92),18,(23,63,78),(64,121,134),2)
    text(d,(51,39),'修正は「1点」に絞る',31,accent,True)
    text(d,(753,46),'実演 / 架空例',23,(177,214,226),True)
    rr(d,(44,133,908,332),26,(42,30,50),(139,85,107),3)
    rr(d,(69,155,233,209),14,(97,45,70))
    text(d,(88,165),'BEFORE',28,(255,207,219),True)
    text(d,(77,230),f'「{VAGUE}」',48,white,True)
    if t>=BEATS[0]:
        p=smooth((t-BEATS[0])/.28)
        d.line((80,303,80+int(340*p),303),fill=(255,139,161),width=5)
        if p>.8: text(d,(640,249),'何を直す？',28,(255,178,198),True)
    p=smooth((t-BEATS[0])/.35)
    d.line((472,343,472,365+int(29*p)),fill=accent,width=5)
    d.polygon(((459,390),(485,390),(472,407)),fill=accent)
    rr(d,(44,417,908,656),27,(14,49,64),mix((47,95,111),accent,smooth((t-BEATS[1])/.55)),4)
    rr(d,(69,438,208,491),13,(27,91,98))
    text(d,(89,448),'AFTER',28,accent,True)
    n=visible_chars(t)
    if n:
        text(d,(78,516),'「'+SPECIFIC[:n]+('」' if n==len(SPECIFIC) else ''),44,white,True)
        if n<len(SPECIFIC) and int(t*5)%2==0:
            x=100+min(690,n*44)
            d.line((x,512,x,571),fill=accent,width=4)
    else: text(d,(79,519),'ここに具体的な修正を書く',35,(143,184,197))
    for i,(lab,sub) in enumerate((('対象','見出し'),('変更','短くする'),('範囲','1点だけ'))):
        p=smooth((t-(BEATS[2]+i*.24))/.24);x=70+i*292
        rr(d,(x,690,x+265,762),15,mix((19,44,60),(28,88,92),p),mix((50,89,105),accent,p),2)
        text(d,(x+15,708),lab,25,mix((133,166,180),accent,p),True)
        text(d,(x+91,707),sub,26,mix((136,168,181),white,p),True)
    return im
