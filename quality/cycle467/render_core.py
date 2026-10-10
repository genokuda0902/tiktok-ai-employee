"""Cycle467 synthetic scene drawing primitives. No external assets or publishing."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from quality_contract import validate, caption_safe
P = json.loads(Path(__file__).with_name('scene_plan.json').read_text(encoding='utf8'))
validate(P)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def frame_at(seconds):
    scene = next(s for s in P['scenes'] if s['start'] <= seconds < s['end'])
    im = Image.new('RGB', (720,1280), '#0b1b35')
    d = ImageDraw.Draw(im)
    def put(xy, value, size=32, color='#ffffff'):
        d.text(xy, value, font=ImageFont.truetype(BOLD,size), fill=color)
    d.rounded_rectangle((36,30,684,125), radius=16, fill='#11344d', outline='#4c9fa8', width=3)
    put((52,52),'AI時短ラボ',35,'#80f4e1')
    put((48,250),scene['title'],39)
    d.rounded_rectangle((46,354,675,942),radius=26,fill='#153b56',outline='#6be9d8',width=3)
    put((76,430),scene['stage'],45,'#6be9d8')
    put((76,540),scene['caption'],32)
    rect=(40,1005,680,1115)
    assert caption_safe(rect)
    d.rounded_rectangle(rect,radius=16,fill='#091e30',outline='#6be9d8',width=3)
    put((65,1042),scene['caption'],27)
    put((45,1175),'SYNTHETIC / REVIEW ONLY',18,'#c1d2de')
    return im
