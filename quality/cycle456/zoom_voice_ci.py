#!/usr/bin/env python3
"""Cycle456: 10-genre-ready mobile zoom-callout and zero-cost Japanese TTS CI.
Only synthetic data. No publishing, paid APIs, or user data.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'cycle455'))
import render_ci as prior

FOCUS={
  2:('選択範囲','E2:E7'),
  3:('数式','=SUM(E2:E7)'),
  4:('セル E3','2 → 4'),
  5:('合計','17 → 19'),
}
original=prior.draw_slide
def draw_slide(i,path):
    original(i,path)
    if i not in FOCUS:
        return
    im=Image.open(path).convert('RGB')
    d=ImageDraw.Draw(im)
    title,value=FOCUS[i]
    d.rounded_rectangle((65,1328,1015,1424),radius=23,fill='#10253C')
    d.rounded_rectangle((81,1342,335,1410),radius=17,fill='#39DDC4')
    d.text((102,1356),title,font=prior.font(30),fill='#10253C')
    size=52 if len(value)<12 else 39
    d.text((372,1343),value,font=prior.font(size),fill='white')
    im.save(path)
prior.draw_slide=draw_slide
prior.ROOT=HERE
if __name__=='__main__':
    prior.main()
