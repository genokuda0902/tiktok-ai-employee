from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def make_footer(output, width=1080, height=1920):
    im=Image.new("RGBA",(width,height),(0,0,0,0))
    d=ImageDraw.Draw(im)
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    bold="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    d.rounded_rectangle((42,1235,1038,1760),radius=42,fill=(3,35,39,255),outline=(75,139,137,255),width=3)
    d.rounded_rectangle((88,1280,370,1340),radius=18,fill=(28,92,91,255))
    d.text((109,1286),"REVIEW ONLY",font=ImageFont.truetype(font,31),fill="#b7f5e7")
    d.text((88,1380),"見やすさを確認",font=ImageFont.truetype(bold,62),fill="white")
    d.text((88,1490),"文字の大きさ  ・  余白  ・  テンポ",font=ImageFont.truetype(font,37),fill="#d2e7e5")
    d.line((88,1595,992,1595),fill="#3c7975",width=3)
    d.text((88,1635),"社内レビュー用  /  公開品質は未承認",font=ImageFont.truetype(font,33),fill="#f3d58a")
    im.save(output)

if __name__=="__main__":
    make_footer(Path("footer.png"))
