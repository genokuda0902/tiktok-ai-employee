"""Offline TikTok scene-4 focus highlights; inherited media stays local."""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
W,H=1080,1920
MARKERS=[
    {'name':'電源','center':(200,870),'color':(251,190,72)},
    {'name':'画面','center':(470,870),'color':(102,191,249)},
    {'name':'入力','center':(735,870),'color':(199,156,236)},
]
STAGES=[(6.00,7.03,-1),(7.03,7.35,0),(7.35,7.67,1),(7.67,8.00,2)]

def overlay(stage:int)->Image.Image:
    if stage not in [-1,0,1,2]: raise ValueError(stage)
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    if stage==-1: return im
    glow=Image.new('RGBA',(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    dr=ImageDraw.Draw(im)
    x,y=MARKERS[stage]['center']
    c=MARKERS[stage]['color']
    gd.ellipse((x-60,y-60,x+60,y+60),fill=(*c,100))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(radius=13)))
    dr.ellipse((x-53,y-53,x+53,y+53),outline=(*c,236),width=7)
    dr.ellipse((x-60,y-60,x+60,y+60),outline=(*c,95),width=2)
    alpha=im.getchannel('A')
    ImageDraw.Draw(alpha).rectangle((800,0,W,H),fill=0)
    im.putalpha(alpha)
    return im

def generate_assets(out:Path):
    out.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i in [-1,0,1,2]:
        p=out/f'focus_{"intro" if i==-1 else i+1}.png'
        overlay(i).save(p,optimize=True)
        paths.append(p)
    return paths

def render(input_mp4:Path,output_mp4:Path,assets:Path):
    paths=generate_assets(assets)
    output_mp4.parent.mkdir(parents=True,exist_ok=True)
    args=['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(input_mp4)]
    for p in paths: args+=['-loop','1','-i',str(p)]
    filt='[0:v]format=yuv420p[base];'
    prev='base'
    for j,(st,en,idx) in enumerate(STAGES):
        target=f'v{j}'
        filt+=f'[{prev}][{j+1}:v]overlay=0:0:format=auto:enable=\'gte(t,{st})*lt(t,{en})\':shortest=1[{target}];'
        prev=target
    filt+=f'[{prev}]format=yuv420p[out]'
    args+=['-filter_complex',filt,'-map','[out]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
           '-r','30','-c:a','copy','-movflags','+faststart',str(output_mp4)]
    subprocess.run(args,check=True)
    return output_mp4

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',default=str(ROOT/'input/previous.mp4'))
    parser.add_argument('--output',default=str(ROOT/'output/cycle756_CONNECTION_FOCUS_HUMAN_REVIEW.mp4'))
    args=parser.parse_args()
    print(render(Path(args.input),Path(args.output),ROOT/'assets'))

if __name__=='__main__':main()
