"""cycle758: Original visual hook, designed as reusable 9:16 image-slide pattern.

No external assets. All images are PIL-generated; inherited narration remains unchanged.
Three cue-aligned stages for the first two seconds replace the old static opener.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
try:
    from scene3_editorial import W,H,WHITE,MUTED,TEAL,CYAN,YELLOW,font,text,rounded
except ModuleNotFoundError:
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'cycle757'/'src'))
    from scene3_editorial import W,H,WHITE,MUTED,TEAL,CYAN,YELLOW,font,text,rounded
ROOT=Path(__file__).resolve().parents[1]
STAGES=[(0.0,0.167,0),(0.167,1.0,1),(1.0,2.0,2)]
BG=(3,13,30)

def board_art():
    """Draw an original, generic PCB diagram (not a branded product image)."""
    s=800
    im=Image.new('RGBA',(s,s),(0,0,0,0)); d=ImageDraw.Draw(im)
    rounded(d,(83,127,731,641),(4,28,42),(36,206,184),34,9)
    rounded(d,(100,144,712,621),(4,52,63),(19,116,112),27,4)
    for i in range(14):
        x=128+i*41
        d.rectangle((x,624,x+25,650),fill=(235,189,95))
    for i in range(9):
        y=190+i*44
        d.line([(132,y),(220,y),(245+int(i%3)*12,y+12)],fill=(26,137,129),width=5,joint='curve')
        d.ellipse((127,y-6,139,y+6),fill=(75,224,195))
        d.line((594,230+i*36,679,230+i*36),fill=(21,131,129),width=4)
    for row in range(4):
        for col in range(4):
            x=122+col*40; y=448+row*38
            d.rectangle((x,y,x+17,y+17),fill=(20,107,107),outline=(57,164,152),width=2)
    rounded(d,(275,245,550,517),(8,27,46),(117,252,225),25,7)
    rounded(d,(298,266,529,496),(7,45,58),(24,133,124),15,3)
    for i in range(11):
        p=288+i*23
        d.rectangle((p,231,p+12,246),fill=(234,190,93))
        d.rectangle((p,518,p+12,533),fill=(234,190,93))
    for i in range(10):
        p=266+i*25
        d.rectangle((261,p,275,p+11),fill=(234,190,93))
        d.rectangle((552,p,565,p+11),fill=(234,190,93))
    d.text((412,366),'CPU',font=font(70,True),fill=WHITE,anchor='mm')
    d.text((412,434),'COMPUTER',font=font(21,True),fill=(101,207,198),anchor='mm')
    for i in range(3):
        rounded(d,(590,290+i*91,675,347+i*91),(7,28,39),(31,139,133),8,2)
    return im.rotate(10,resample=Image.Resampling.BICUBIC,expand=True)

def gradient_bg():
    im=Image.new('RGB',(W,H),BG)
    px=im.load()
    for y in range(H):
        for x in range(W):
            dist=((x-580)**2/(680**2)+(y-840)**2/(850**2))
            light=max(0,1-dist)*0.65
            px[x,y]=(int(3+9*light),int(13+37*light),int(30+42*light))
    return im.convert('RGBA')

def scene_image(stage:int)->Image.Image:
    if stage not in (0,1,2): raise ValueError(stage)
    im=gradient_bg(); d=ImageDraw.Draw(im)
    for x in range(50,W,75): d.line((x,210,x,1320),fill=(10,36,51),width=2)
    for y in range(210,1330,75): d.line((50,y,1030,y),fill=(10,36,51),width=2)
    rounded(d,(55,55,397,139),(6,75,78),TEAL,20,3)
    text(d,(80,76),'15秒でわかる',38,WHITE,True)
    text(d,(931,94),'01 / 08',29,MUTED,False,'mm')
    rounded(d,(55,172,1023,185),(19,67,73),None,7)
    rounded(d,(55,172,175,185),TEAL,None,7)
    text(d,(64,252),'この小さな基板、',66,WHITE,True)
    if stage==2:
        text(d,(64,359),'実はパソコン。',94,YELLOW,True)
        text(d,(68,489),'手のひらに、コンピューター。',33,MUTED)
    else:
        text(d,(64,359),'正体は…？',94,TEAL,True)
        text(d,(68,489),'見た目だけで判断できない。',33,MUTED)
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(gl)
    gd.ellipse((148,628,938,1290),fill=(16,182,159,95 if stage==2 else 50))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(115)))
    art=board_art()
    art.thumbnail((800,800),Image.Resampling.LANCZOS)
    im.alpha_composite(art,((W-art.width)//2,605))
    d=ImageDraw.Draw(im)
    if stage==2:
        rounded(d,(128,1164,953,1273),(11,94,94),(105,252,210),23,4)
        text(d,(540,1217),'CPU ＋ メモリ ＝ コンピューター',37,WHITE,True,'mm')
    else:
        rounded(d,(186,1164,896,1273),(8,52,67),(50,158,158),23,3)
        text(d,(540,1217),'何に使う部品だと思う？',43,WHITE,True,'mm')
    rounded(d,(55,1360,1025,1572),(5,40,57),TEAL,29,4)
    rounded(d,(81,1381,270,1423),(10,88,91),None,10)
    text(d,(105,1385),'VOICE / JP',25,WHITE,True)
    caption='' if stage==0 else ('この基板、' if stage==1 else '実はパソコン。')
    text(d,(540,1490),caption,68,WHITE,True,'mm')
    rounded(d,(90,1533,987,1545),(20,77,87),None,5)
    rounded(d,(90,1533,90+(370 if stage<2 else 805),1545),TEAL,None,5)
    text(d,(65,1633),'ORIGINAL VECTOR ART / HUMAN REVIEW',23,(110,153,163))
    return im.convert('RGB')

def render(input_mp4:Path,output_mp4:Path,assets:Path):
    assets.mkdir(parents=True,exist_ok=True); output_mp4.parent.mkdir(parents=True,exist_ok=True)
    for stage in range(3): scene_image(stage).save(assets/f'hook_{stage}.png',optimize=True)
    cmd=['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(input_mp4)]
    for stage in range(3):cmd+=['-loop','1','-i',str(assets/f'hook_{stage}.png')]
    f='[0:v]format=yuv420p[v0];'; prev='v0'
    for i,(start,end,stage) in enumerate(STAGES):
        f+=f"[{prev}][{i+1}:v]overlay=0:0:enable='gte(t,{start})*lt(t,{end})':shortest=1[v{i+1}];"
        prev=f'v{i+1}'
    f+=f'[{prev}]format=yuv420p[out]'
    cmd+=['-filter_complex',f,'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output_mp4)]
    subprocess.run(cmd,check=True)
    return output_mp4

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',default=str(ROOT/'input/previous.mp4'))
    p.add_argument('--output',default=str(ROOT/'output/cycle758_HOOK_REVEAL_HUMAN_REVIEW.mp4'))
    a=p.parse_args()
    print(render(Path(a.input),Path(a.output),ROOT/'assets'))
