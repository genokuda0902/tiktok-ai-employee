from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(n,bold=True):return ImageFont.truetype(FONT if bold else REG,n)
def draw_overlay(genre,out):
    themes=json.loads((HERE/'config/genres.json').read_text())['genres']
    color=themes[genre]['theme']
    im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((44,1000,1036,1765),radius=40,fill=(5,25,37,255),outline=color,width=5)
    d.rounded_rectangle((76,1034,366,1094),radius=28,fill=(17,62,68,255))
    d.text((104,1044),'保存用・3ステップ',font=font(28),fill=color)
    d.text((78,1110),'これだけ覚えておこう',font=font(54),fill='white')
    for (num,label),x in zip([('01','準備'),('02','起動'),('03','制作')],[76,392,708]):
        d.rounded_rectangle((x,1218,x+294,1470),radius=26,fill=(14,47,64,255),outline=(53,98,105,255),width=3)
        d.ellipse((x+107,1244,x+187,1324),fill=color)
        for txt,y,size,fg in [(num,1260,35,'#001B25'),(label,1351,57,'white')]:
            f=font(size);b=d.textbbox((0,0),txt,font=f)
            d.text((x+147-(b[2]-b[0])/2,y),txt,font=f,fill=fg)
    d.rounded_rectangle((76,1510,1004,1630),radius=29,fill=color)
    cta='保存して、あとで試す';f=font(49);b=d.textbbox((0,0),cta,font=f)
    d.text((540-(b[2]-b[0])/2,1537),cta,font=f,fill='#06242C')
    d.text((88,1692),'※ 音声終了後のまとめ｜ナレーション字幕ではありません',font=font(25,False),fill='#A6C1C6')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);im.save(out,optimize=True)
    return color
