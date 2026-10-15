"""Generated 9:16 animated proof card. No external image assets."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from proof_model import SAMPLE
W,H=1080,1920
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(n,b=True): return ImageFont.truetype(B if b else R,n)
def rr(d,box,color,r=18,outline=None):
    d.rounded_rectangle(tuple(map(int,box)),radius=r,fill=color,outline=outline,width=3)
def ease(v):
    v=max(0,min(1,v))
    return 1-(1-v)**3
def frame(index,count=72,proof=SAMPLE):
    proof.validate()
    p=index/max(1,count-1)
    im=Image.new('RGB',(W,H),(7,22,37))
    d=ImageDraw.Draw(im)
    for y in range(H):
        z=y/H
        d.line((0,y,W,y),fill=(int(7+6*z),int(22+14*z),int(37+24*z)))
    glow=Image.new('RGBA',(W,H),(0,0,0,0))
    g=ImageDraw.Draw(glow)
    cx=720+80*math.sin(p*5)
    cy=430+55*math.sin(p*3)
    g.ellipse((cx-240,cy-240,cx+240,cy+240),fill=(0,215,202,42))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(110)))
    d=ImageDraw.Draw(im)
    rr(d,(55,90,1025,166),(13,77,89),20)
    d.text((85,103),'AI時短ラボ   /   検証デモ',font=f(35),fill='white')
    d.text((70,252),'数字の根拠を',font=f(85),fill='white')
    d.text((70,364),'目で確認する。',font=f(85),fill=(51,242,204))
    d.text((75,500),'4か月のデータを検算',font=f(43,False),fill=(188,219,229))
    rr(d,(72,600,1008,614),(25,60,75),7)
    rr(d,(72,600,72+936*ease(p),614),(28,213,218),7)
    rr(d,(60,690,1020,1480),(237,248,250),38)
    rr(d,(60,690,1020,773),(23,100,110),35)
    d.rectangle((60,739,1020,773),fill=(23,100,110))
    d.text((94,701),'元データ → 計算式 → 結果',font=f(39),fill='white')
    for i,(label,value) in enumerate(zip(proof.labels,proof.values)):
        x=135+i*230 if len(proof.values)==4 else 110+i*810/max(1,len(proof.values)-1)
        growth=ease((p-.10-i*.11)/.20)
        h=value/max(proof.values)*250*growth
        rr(d,(x,1260-h,x+95,1260),(26,222,168) if value==max(proof.values) else (26,156,204),16)
        if growth>.05:
            d.text((x-3,1198-h),str(value),font=f(40),fill=(16,61,74))
        d.text((x+7,1290),label,font=f(36),fill=(26,62,73))
    rr(d,(85,1365,995,1447),(210,246,232),16)
    message=f'合計  {proof.total}' if p>=.45 else '合計を検算中…'
    d.text((108,1376),message,font=f(47),fill=(15,103,82))
    rr(d,(72,1530,1008,1695),(14,67,78),22,(33,184,181))
    if p>=.70: message=f'最大値は{proof.peak}  {max(proof.values)}'
    elif p>=.32: message='入力値とグラフを照合'
    else: message='4つの数値を順番に確認'
    d.text((108,1572),message,font=f(46),fill='white')
    d.text((78,1770),'架空データによる演出 / 実操作・AI解析ではありません',font=f(27,False),fill=(177,199,212))
    return im.convert('RGB')
