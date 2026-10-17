from PIL import Image, ImageFont
from before_after_card import draw_before_after

def test_illustrative_comparison():
    im = Image.new('RGB', (540,960), '#08162e')
    def paint(d,x,y,s,size,color):
        d.text((x,y),s,fill=color,font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',size))
    r = draw_before_after(im,paint)
    assert r['illustrative_only'] is True
    assert '検算' in r['disclaimer']
    assert im.getpixel((60,300)) != im.getpixel((300,300))
