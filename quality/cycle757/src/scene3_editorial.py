"""cycle757: Original, reusable 9:16 editorial image-slide renderer.

Three narration-aligned scene states replace a cluttered 4.0-6.0s screen.
Only PIL-created vector illustrations and locally installed Japanese fonts are used.
All other video scenes and the inherited AAC audio stream are preserved.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
W,H=1080,1920
BG=(4,15,31)
WHITE=(245,251,255)
MUTED=(165,193,210)
TEAL=(62,233,205)
CYAN=(93,193,246)
YELLOW=(255,201,101)
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# 60 frames = 2 seconds. Two narration cues start at 4.033 and 5.100.
STAGES=[(4.0,4.45,0),(4.45,5.10,1),(5.10,6.0,2)]

def font(size:int,bold:bool=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)

def text(draw,xy,s,size,color=WHITE,bold=False,anchor=None):
    draw.text(xy,s,font=font(size,bold),fill=color,anchor=anchor,stroke_width=0)

def rounded(draw,box,fill,outline=None,r=24,width=2):
    draw.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def glow_rect(im,box,color=TEAL,radius=26,blur=26):
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    d.rounded_rectangle(box,radius=radius,outline=(*color,170),width=7)
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))

def draw_board(d,stage):
    # Original flat-vector circuit-board drawing; no third-party illustration.
    x0,y0,x1,y1=105,740,368,1040
    rounded(d,(x0,y0,x1,y1),(8,62,65),TEAL,22,4)
    for i in range(5):
        yy=y0+44+i*49
        d.line((x0+30,yy,x0+80,yy),fill=(35,136,134),width=3)
        d.line((x1-75,yy,x1-28,yy),fill=(35,136,134),width=3)
    rounded(d,(161,807,312,923),(5,26,41),(164,255,233),16,4)
    text(d,(236,844),'CPU',48,WHITE,True,'mm')
    for i in range(6):
        px=168+i*23
        d.rectangle((px,797,px+12,806),fill=YELLOW)
        d.rectangle((px,924,px+12,933),fill=YELLOW)
    for i in range(3):
        d.rectangle((126+i*72,981,174+i*72,1001),fill=(48,173,163))
    text(d,(236,1079),'小さな基板',33,MUTED,False,'mm')
    text(d,(236,1128),'CPU・メモリ搭載',24,(113,181,187),False,'mm')

def draw_monitor(d,stage):
    mx0,my0,mx1,my1=502,701,914,1048
    rounded(d,(mx0,my0,mx1,my1),(5,31,49),TEAL if stage>0 else (70,118,131),25,5)
    rounded(d,(520,720,896,1008),(5,18,34),(30,92,104),13,2)
    if stage==0:
        text(d,(708,843),'画面を接続',38,MUTED,True,'mm')
        d.ellipse((683,899,733,949),outline=(70,130,146),width=4)
    elif stage==1:
        rounded(d,(545,746,871,970),(9,53,68),(62,233,205),16,3)
        rounded(d,(565,770,851,804),(18,91,98),None,9)
        for i,c in enumerate([(255,110,116),(255,210,119),(91,221,168)]):
            d.ellipse((584+i*29,781,598+i*29,795),fill=c)
        text(d,(708,868),'接続完了',47,WHITE,True,'mm')
        text(d,(708,929),'画面が起動',26,TEAL,False,'mm')
    else:
        rounded(d,(545,746,871,970),(9,53,68),(62,233,205),16,3)
        rounded(d,(565,770,851,804),(18,91,98),None,9)
        for i,c in enumerate([(255,110,116),(255,210,119),(91,221,168)]):
            d.ellipse((584+i*29,781,598+i*29,795),fill=c)
        text(d,(708,866),'操作できる',46,WHITE,True,'mm')
        rounded(d,(606,908,808,955),(20,118,111),TEAL,14,2)
        text(d,(707,930),'✓ 画面で操作',24,WHITE,True,'mm')
    d.line((684,1052,684,1094),fill=(106,173,184),width=11)
    rounded(d,(616,1091,752,1110),(64,135,146),None,9)
    text(d,(708,1145),'ディスプレイ',31,MUTED,False,'mm')

def draw_cable(d,stage):
    # Route a connection through the central blank column.
    if stage==0:
        d.line([(369,900),(430,900)],fill=(75,130,144),width=11)
        d.ellipse((420,890,440,910),fill=YELLOW)
    else:
        d.line([(369,900),(442,900),(442,875),(500,875)],fill=TEAL,width=13,joint='curve')
        d.ellipse((430,862,456,888),fill=YELLOW,outline=WHITE,width=2)
        d.polygon([(478,861),(501,875),(478,889)],fill=TEAL)

def scene_image(stage:int)->Image.Image:
    if stage not in (0,1,2): raise ValueError('stage must be 0,1,2')
    im=Image.new('RGBA',(W,H),BG+(255,))
    d=ImageDraw.Draw(im)
    for x in range(30,W,68):
        d.line((x,155,x,1630),fill=(9,29,45),width=2)
    for y in range(155,1640,68):
        d.line((30,y,1020,y),fill=(9,29,45),width=2)
    # Small top progress header
    rounded(d,(52,56,388,137),(5,74,80),TEAL,21,3)
    text(d,(80,76),'15秒でわかる',37,WHITE,True)
    text(d,(840,86),'03 / 08',30,MUTED,False,'mm')
    rounded(d,(52,166,1028,181),(22,68,79),None,7)
    rounded(d,(52,166,405,181),TEAL,None,7)
    # Headline: short, high-contrast and legible at phone size
    text(d,(58,251),'画面につなぐと、',63,WHITE,True)
    text(d,(58,344),'小さな基板が動き出す。',60,TEAL,True)
    text(d,(60,438),'接続から操作まで、たった2ステップ',29,MUTED)
    # Two clear cards replace nested tiny screenshots
    glow_rect(im,(68,573,966,1230),TEAL if stage>0 else CYAN,30,18)
    d=ImageDraw.Draw(im)
    rounded(d,(68,573,966,1230),(4,32,49), (31,137,137),31,3)
    rounded(d,(96,595,374,656),(12,76,82),None,16)
    text(d,(235,623),'01 / 接続',29,WHITE,True,'mm')
    rounded(d,(660,595,936,656),(12,76,82),None,16)
    text(d,(798,623),'02 / 操作',29,WHITE,True,'mm')
    draw_board(d,stage)
    draw_cable(d,stage)
    draw_monitor(d,stage)
    # Bottom one-line takeaway inside the visual frame
    rounded(d,(110,1169,924,1211),(8,67,75),None,13)
    label=['基板と画面をつなぐ','画面が起動する','キーボードで操作できる'][stage]
    text(d,(518,1189),label,29,WHITE,True,'mm')
    # Caption panel; original SRT cue boundaries are maintained in the 2-state render.
    rounded(d,(52,1345,966,1565),(3,37,55),TEAL,27,4)
    rounded(d,(78,1368,270,1407),(13,89,94),None,10)
    text(d,(100,1372),'VOICE / JP',25,WHITE,True)
    text(d,(900,1387),'03 / 08',24,MUTED,False,'mm')
    caption='画面につなげば、' if stage<2 else '操作できる。'
    text(d,(508,1462),caption,62,WHITE,True,'mm')
    rounded(d,(84,1530,934,1541),(23,83,92),None,5)
    rounded(d,(84,1530,84+(400 if stage<2 else 780),1541),TEAL,None,5)
    text(d,(58,1630),'CONCEPT ART / HUMAN REVIEW',23,(121,156,168))
    # Keep x>=970 and y>=1660 free for native TikTok UI.
    return im.convert('RGB')

def render(input_mp4:Path, output_mp4:Path, asset_dir:Path):
    asset_dir.mkdir(parents=True,exist_ok=True)
    output_mp4.parent.mkdir(parents=True,exist_ok=True)
    for stage in range(3):
        scene_image(stage).save(asset_dir/f'scene3_{stage}.png',optimize=True)
    args=['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(input_mp4)]
    for stage in range(3):
        args+=['-loop','1','-i',str(asset_dir/f'scene3_{stage}.png')]
    filt='[0:v]format=yuv420p[v0];'
    prev='v0'
    for i,(start,end,stage) in enumerate(STAGES):
        filt+=f"[{prev}][{i+1}:v]overlay=0:0:enable='gte(t,{start})*lt(t,{end})':shortest=1[v{i+1}];"
        prev=f'v{i+1}'
    filt+=f'[{prev}]format=yuv420p[out]'
    args+=['-filter_complex',filt,'-map','[out]','-map','0:a:0','-c:v','libx264',
           '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30',
           '-c:a','copy','-movflags','+faststart',str(output_mp4)]
    subprocess.run(args,check=True)
    return output_mp4

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',default=str(ROOT/'input/previous.mp4'))
    p.add_argument('--output',default=str(ROOT/'output/cycle757_EDITORIAL_SCENE3_HUMAN_REVIEW.mp4'))
    args=p.parse_args()
    print(render(Path(args.input),Path(args.output),ROOT/'assets'))

if __name__=='__main__':main()
