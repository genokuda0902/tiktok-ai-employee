"""Native portrait image-first outro frames. Review-only; no posting."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from outro_contract import GENRES, WIDTH, HEIGHT, CAPTION, SAFE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def font(size):
    return ImageFont.truetype(FONT, size)

def frame(hero, index, genre):
    if genre not in GENRES or not 0 <= index < 90:
        raise ValueError("invalid genre/frame")
    accent = tuple(bytes.fromhex(GENRES[genre][1:]))
    p = index / 89
    im = Image.new("RGB", (WIDTH, HEIGHT), "#061426")
    d = ImageDraw.Draw(im)
    for y in range(HEIGHT):
        t = y / HEIGHT
        d.line((0,y,WIDTH,y), fill=(int(6+4*t),int(20+12*t),int(41+15*t)))
    d.ellipse((660,330,1450,1130),fill=(11,55,80))
    d.ellipse((-340,910,420,1670),fill=(11,42,64))
    d.rounded_rectangle((86,196,442,262),radius=26,outline=accent,width=3,fill=(5,28,45))
    d.text((110,208),"AI時短ラボ  /  SAVE",font=font(31),fill="white")
    d.text((87,315),"次は、あなたの番。",font=font(74),fill="white")
    d.text((89,435),"この手順を、あとで再現。",font=font(43),fill=(167,222,225))
    d.rounded_rectangle((117,570,987,1242),radius=50,fill=(1,7,18))
    crop=hero.crop((110,560,990,1190)).convert("RGB")
    scale=1.04+0.04*(1-(1-p)**3)
    w,h=int(870*scale),int(670*scale)
    crop=crop.resize((w,h),Image.Resampling.LANCZOS)
    ox=max(0,(w-870)//2+int(10*math.sin(math.pi*p)))
    oy=max(0,(h-670)//2)
    crop=crop.crop((ox,oy,ox+870,oy+670))
    mask=Image.new("L",(870,670))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,869,669),radius=48,fill=255)
    im.paste(crop,(105,550),mask)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((105,550,975,1220),radius=48,outline=accent,width=5)
    for j,(x0,x1) in enumerate([(102,376),(402,676),(702,976)]):
        active=p>=0.08+j*0.19
        d.rounded_rectangle((x0,1250,x1,1374),radius=25,
            fill=(9,47,64) if active else (10,30,46),
            outline=accent if active else (41,72,84),width=3)
        label=f"{j+1}  {['表を用意','AIに指示','Excelで確認'][j]}"
        d.text((x0+21,1284),label,font=font(30),
               fill="white" if active else (137,166,180))
    d.rounded_rectangle((92,1430,988,1580),radius=34,
                        fill=(1,13,26),outline=accent,width=5)
    cta_font=font(57)
    width=d.textbbox((0,0),CAPTION,font=cta_font)[2]
    x=(WIDTH-width)//2
    if x<SAFE[0] or x+width>SAFE[2]:
        raise ValueError("CTA outside safe zone")
    d.text((x,1472),CAPTION,font=cta_font,fill="white")
    d.text((93,1680),"※ 架空データ・操作イメージ｜公開未承認",
           font=font(27),fill=(138,165,176))
    return im
