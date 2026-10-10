#!/usr/bin/env python3
"""Cycle457 CI candidate: chart overlay + genuine free Japanese TTS, no posting.
The locally shared cycle457 preview has a richer 5-stage chart but SFX only.
This script must FAIL if real Japanese narration cannot be generated.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'cycle455'))
import render_ci as previous
ORIGINAL=previous.draw_slide
BEFORE=[3,2,4,1,5,2]
AFTER=[3,4,4,1,5,2]
assert sum(BEFORE)==17 and sum(AFTER)==19
def draw_slide(i,path):
    ORIGINAL(i,path)
    if i!=5:return
    im=Image.open(path).convert('RGB')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((82,665,996,1300),radius=30,fill='#FFFFFF',outline='#DAE6EF',width=5)
    d.text((126,702),'変更前 / 変更後',font=previous.font(46),fill='#13243B')
    baseline=1160
    for x,value,label,color in ((250,17,'変更前','#A8BDD2'),(650,19,'変更後','#38D9C4')):
        top=int(baseline-value*17)
        d.rounded_rectangle((x,top,x+170,baseline),radius=18,fill=color)
        d.text((x+38,top-70),str(value),font=previous.font(48),fill='#13243B')
        d.text((x+12,1180),label,font=previous.font(34),fill='#13243B')
    d.text((280,1250),'合計 +2 件',font=previous.font(42),fill='#1A6357')
    im.save(path)
previous.draw_slide=draw_slide
previous.ROOT=HERE
if __name__=='__main__':
    previous.main()
