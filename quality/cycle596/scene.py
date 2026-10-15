"""Original, rights-clean scene illustration for the cycle596 review candidate."""
from PIL import Image, ImageDraw, ImageFont
from .proof_contract import proof
W,H,FPS=1080,1920,30
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def label(d,xy,s,size=36,color="white",max_width=930):
    f=ImageFont.truetype(FONT,size)
    b=d.textbbox(xy,s,font=f)
    if b[2]-b[0]>max_width:raise ValueError("text overflow: "+s)
    d.text(xy,s,font=f,fill=color)
def frame(t,values=(120,150,200,250),genre="AI・仕事効率化"):
    p=proof(values,genre);total=p["total"]
    im=Image.new("RGB",(W,H),(6,17,31));d=ImageDraw.Draw(im)
    d.ellipse((780,-280,1260,200),outline=(21,78,96),width=5)
    d.rounded_rectangle((58,155,1022,238),radius=20,fill=(16,62,79),outline=(42,156,167),width=2)
    label(d,(88,167),"AI時短ラボ  /  数字で確認する BEFORE → AFTER",34)
    label(d,(67,290),"同じ4件の入力。結果は一致する？",59)
    label(d,(70,393),genre+"  /  架空データで検算",32,(156,199,212))
    for j,(x0,y0,x1,y1) in enumerate(((65,493,516,1250),(564,493,1015,1250))):
        accent=(247,138,160) if j==0 else (39,224,193)
        d.rounded_rectangle((x0,y0,x1,y1),radius=30,fill=(20,37,56) if j==0 else (11,53,58),outline=accent,width=4)
        d.rounded_rectangle((x0+20,y0+23,x1-20,y0+115),radius=19,fill=(83,38,54) if j==0 else (8,93,87))
        label(d,(x0+42,y0+40),"BEFORE  手で足す" if j==0 else "AFTER  関数で検算",39,max_width=390)
    count=min(4,max(1,int(t/.38)+1));running=0
    for i,v in enumerate(values):
        running+=v;y=658+i*110
        if i<count:
            d.rounded_rectangle((94,y-8,480,y+88),radius=16,fill=(48,48,69))
            label(d,(117,y+10),f"{i+1}件目  +{v}",32,(234,225,233),220)
            label(d,(345,y+9),str(running),43,(255,208,219),120)
        else:label(d,(125,y+15),f"{i+1}件目  …",34,(105,125,147),260)
    d.rounded_rectangle((591,648,989,1002),radius=18,fill=(232,246,247))
    d.rectangle((591,648,989,707),fill=(36,93,104))
    label(d,(613,657),"セル",30,max_width=100)
    label(d,(803,657),"値",30,max_width=100)
    for i,v in enumerate(values):
        y=718+i*68
        if i%2==0:d.rectangle((601,y-5,979,y+56),fill=(213,237,239))
        label(d,(619,y),f"B{i+2}",34,(32,65,79),130)
        label(d,(799,y),str(v),34,(26,60,70),150)
    d.rounded_rectangle((592,1030,989,1125),radius=15,fill=(3,28,34),outline=(62,198,181),width=3)
    label(d,(616,1049),"=SUM(B2:B5)",42,max_width=360)
    if t>=1.08:
        d.rounded_rectangle((588,1145,993,1220),radius=16,fill=(16,110,95))
        label(d,(612,1155),f"合計  {total}",48,max_width=350)
    else:label(d,(610,1160),"値を検証中…",34,(173,220,216),350)
    caption="左は順番に加算。右はSUM関数。" if t<1.08 else f"どちらも合計 {total}。数字で確認。"
    f=ImageFont.truetype(FONT,48);bb=d.textbbox((0,0),caption,font=f);cw=bb[2]-bb[0]
    if cw>900:raise ValueError("caption overflow")
    d.rounded_rectangle((70,1310,1010,1450),radius=26,fill=(12,74,86),outline=(55,203,192),width=3)
    d.text(((W-cw)//2,1342),caption,font=f,fill="white")
    d.rounded_rectangle((80,1502,1000,1519),radius=8,fill=(24,59,76))
    prog=max(0,min(1,t/1.85));prog=1-(1-prog)**3
    d.rounded_rectangle((80,1502,80+int(920*prog),1519),radius=8,fill=(39,224,193))
    label(d,(80,1602),"架空データによる再現映像  /  REVIEW ONLY",27,(130,174,186))
    p.update({"caption":caption,"caption_box":(70,1310,1010,1450),"partial":sum(values[:count])})
    return im,p
