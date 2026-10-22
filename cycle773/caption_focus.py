#!/usr/bin/env python3
"""Cycle773: offline Japanese subtitle-focus overlay for 1080x1920 H264 MP4.

Usage: python cycle773/caption_focus.py --source previous.mp4 --srt captions.srt --output improved.mp4 --accent '#52EBD0'
Input media rights and approval remain the operator's responsibility. Never posts.
"""
import argparse
import re
import subprocess
from pathlib import Path

FPS = 30
HIGHLIGHTS = ('基板','パソコン','手のひら','本格派','画面','操作','必要','三つ',
              'LED','光らせられる','入力','出力','最初','一行','保存','試そう')

def seconds(ts):
    hh, mm, ss = ts.replace(',', '.').split(':')
    return int(hh)*3600 + int(mm)*60 + float(ss)

def cues_from_srt(path):
    data = Path(path).read_text(encoding='utf-8-sig')
    result = []
    for block in re.split(r'\n\s*\n', data.strip()):
        match = re.search(r'(\d\d:\d\d:\d\d,\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d,\d\d\d)', block)
        if match:
            result.append((seconds(match.group(1)), seconds(match.group(2)),
                           block[match.end():].strip().replace('\n',' ')))
    return result

def frame_cues(cues):
    out=[]
    for start, end, caption in cues:
        a,b=round(start*FPS),round(end*FPS)
        if a>=b or (out and a<out[-1][1]):
            raise ValueError('invalid or overlapping caption times')
        out.append((a,b,caption))
    return out

def ass_time(frame):
    n=round(frame*100/FPS)
    h,n=divmod(n,360000)
    m,n=divmod(n,6000)
    s,cs=divmod(n,100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'

def bgr(rgb):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',rgb):
        raise ValueError('accent must be #RRGGBB')
    return '&H'+rgb[5:7]+rgb[3:5]+rgb[1:3]+'&'

def make_ass(cues, accent, output):
    frames=frame_cues(cues)
    if len(frames)!=16: raise ValueError('16 phrases required')
    if any(word not in phrase for word,(_,_,phrase) in zip(HIGHLIGHTS,frames)):
        raise ValueError('caption keyword missing')
    color=bgr(accent)
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Noto Sans CJK JP,76,&H00FFFFFF,&H00FFFFFF,&H00091C30,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,50,50,0,1
Style: Meta,Noto Sans CJK JP,26,&H00B0CDD8,&H00FFFFFF,&H00091C30,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,30,30,0,1
Style: Bar,Noto Sans CJK JP,18,&H00FFFFFF,&H00FFFFFF,&H00091C30,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines=[]
    for index,(a,b,phrase) in enumerate(frames,1):
        start,end=ass_time(a),ass_time(b)
        key=HIGHLIGHTS[index-1]
        before,after=phrase.split(key,1)
        body=before.replace('{','').replace('}','')+r'{\c'+color+'}'+key+r'{\c&HFFFFFF&}'+after.replace('{','').replace('}','')
        lines.append(f'Dialogue: 2,{start},{end},Main,,0,0,0,,{{\\move(540,1590,540,1575,0,160)\\fad(50,40)}}{body}')
        lines.append(f'Dialogue: 2,{start},{end},Meta,,0,0,0,,{{\\pos(170,1507)}}JAPANESE VOICE')
        lines.append(f'Dialogue: 2,{start},{end},Meta,,0,0,0,,{{\\pos(915,1507)}}{index:02} / 16')
        progress=round(822*index/16)
        lines.append(f'Dialogue: 2,{start},{end},Bar,,0,0,0,,{{\\pos(129,1640)\\p1\\c{color}}}m 0 0 l {progress} 0 {progress} 9 0 9{{\\p0}}')
    Path(output).write_text(header+'\n'.join(lines)+'\n',encoding='utf-8')
    return len(frames)

def render(source, srt, output, accent='#52EBD0'):
    source,output=Path(source).resolve(),Path(output).resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    ass=output.with_suffix('.ass')
    make_ass(cues_from_srt(srt),accent,ass)
    silent=output.with_name(output.stem+'_silent.mp4')
    vf=('drawbox=x=60:y=1475:w=960:h=190:color=0x081b2c@1:t=fill,'
        'drawbox=x=60:y=1475:w=960:h=190:color=0x427b88@0.9:t=3,'
        'drawbox=x=129:y=1640:w=822:h=9:color=0x245163@1:t=fill,'
        f'ass={ass}:fontsdir=/usr/share/fonts/opentype/noto,format=yuv420p')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-map','0:v:0','-an','-vf',vf,'-frames:v','429','-c:v','libx264',
        '-preset','fast','-crf','18','-pix_fmt','yuv420p',str(silent)],check=True)
    try:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-i',str(silent),'-i',str(source),'-map','0:v:0','-map','1:a:0',
            '-c','copy','-movflags','+faststart',str(output)],check=True)
    finally:
        silent.unlink(missing_ok=True)
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--srt',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--accent',default='#52EBD0')
    a=p.parse_args()
    print(render(a.source,a.srt,a.output,a.accent))
