#!/usr/bin/env python3
"""Offline safe-zone Japanese captions for the eight-scene 1080x1920 review sample.
No posting, paid APIs, network, or merges. Audio stream copied unchanged.
Independent ASR and semantic caption alignment are NOT verified.
"""
import argparse, subprocess
from pathlib import Path

GENRES = {'ai_work':'AI時短ワーク','business':'仕事のコツ','money':'お金の知識',
'learning':'学びの習慣','health':'健康の基本','lifestyle':'暮らしの工夫',
'psychology':'心の仕組み','science':'科学の発見','history':'歴史の発見','travel':'旅のヒント'}
SCENES = [
(0,3.133333,'AIで仕事を速くするなら、','最初の一歩が大事。'),
(3.133333,5.6,'まず、繰り返している','作業を書き出す。'),
(5.6,8.233333,'次に、完成形の見本を','用意する。'),
(8.233333,11.,'指示は、目的と条件を','具体的に伝える。'),
(11.,13.733333,'最初の出力は、','必ず自分で確かめる。'),
(13.733333,16.633333,'違いがあれば、修正点を','一つずつ伝える。'),
(16.633333,19.166667,'使える指示は、','テンプレートに残す。'),
(19.166667,22.5,'小さな時短を、','毎日の習慣にしよう。')]
CAPTION_RIGHT, CAPTION_BOTTOM = 880, 1630

def ass_time(t):
    n=round(t*100); h,r=divmod(n,360000); m,r=divmod(r,6000); s,c=divmod(r,100)
    return f'{h}:{m:02}:{s:02}.{c:02}'

def make_ass(dest, scenes=SCENES, genre='ai_work'):
    if genre not in GENRES: raise ValueError('unknown genre')
    if not scenes or abs(scenes[0][0])>.001 or abs(scenes[-1][1]-22.5)>.001:
        raise ValueError('incomplete timeline')
    for i,(start,end,a,b) in enumerate(scenes):
        if not 0<=start<end<=22.50001 or not a or not b: raise ValueError('invalid caption')
        if i and abs(start-scenes[i-1][1])>.001: raise ValueError('scene gap')
    header="""[Script Info]
Title: Offline Japanese captions / HUMAN REVIEW ONLY
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,70,200,0,1
Style: Eyebrow,Noto Sans CJK JP,29,&H00E7D4B5,&H00E7D4B5,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,70,200,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines=[header]
    for i,(start,end,a,b) in enumerate(scenes):
        start,end=ass_time(start),ass_time(end)
        a=a.replace('{','（').replace('}','）')
        b=b.replace('{','（').replace('}','）')
        lines.append(f'Dialogue: 0,{start},{end},Eyebrow,,0,0,0,,{{\\pos(75,1400)}}音声の要点　{i+1:02} / 08\n')
        lines.append(f'Dialogue: 1,{start},{end},Caption,,0,0,0,,{{\\pos(75,1461)}}{a}\\N{{\\c&H00D5E04E&}}{b}\n')
    Path(dest).write_text(''.join(lines),encoding='utf-8')

def command(src,dest,ass,duration=22.5):
    path=str(Path(ass).resolve()).replace(':','\\:')
    vf=("drawbox=x=25:y=1370:w=1040:h=286:color=0x031021@1:t=fill,"
        "drawbox=x=42:y=1378:w=860:h=253:color=0x5ae6db@0.85:t=3,"
        "drawbox=x=42:y=1378:w=8:h=253:color=0x5ae6db@1:t=fill,"
        f"ass=filename='{path}'")
    return ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-vf',vf,
            '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
            '-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','20',
            '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dest)]

def render(src,dest,genre='ai_work',duration=22.5):
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    ass=dest.with_suffix('.ass');make_ass(ass,genre=genre)
    subprocess.run(command(src,dest,ass,duration),check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input_mp4');p.add_argument('output_mp4')
    p.add_argument('--genre',choices=GENRES,default='ai_work');p.add_argument('--duration',type=float,default=22.5)
    a=p.parse_args();render(a.input_mp4,a.output_mp4,a.genre,a.duration)
