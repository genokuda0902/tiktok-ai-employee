#!/usr/bin/env python3
"""Cycle774: offline UI-safe captions for 1080x1920 Japanese image-slide MP4s."""
import argparse, json, re, subprocess
from pathlib import Path
FPS=30
PANEL=(64,1368,884,1552)
RIGHT_RAIL_START=900
BOTTOM_UI_START=1600
KEYWORDS=['基板','パソコン','手のひら','本格派','画面','操作','必要','三つ','LED','光らせられる','入力','出力','最初','一行','保存','試そう']
def sec(s):
    h,m,t=s.replace(',','.').split(':')
    return int(h)*3600+int(m)*60+float(t)
def stamp(frame):
    cs=round(frame*100/FPS);h,r=divmod(cs,360000);m,r=divmod(r,6000);s,c=divmod(r,100)
    return f'{h}:{m:02}:{s:02}.{c:02}'
def read_srt(path):
    out=[]
    for block in re.split(r'\n\s*\n',Path(path).read_text(encoding='utf-8-sig').strip()):
        m=re.search(r'(\d\d:\d\d:\d\d,\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d,\d\d\d)',block)
        if m:out.append((round(sec(m[1])*FPS),round(sec(m[2])*FPS),block[m.end():].strip().replace('\n',' ')))
    return out
def build_ass(cues,accent,path):
    if not (len(cues)==16 and PANEL[2]<RIGHT_RAIL_START and PANEL[3]<BOTTOM_UI_START):raise ValueError('unsafe layout or cue count')
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',accent):raise ValueError('bad accent')
    col='&H'+accent[5:7]+accent[3:5]+accent[1:3]+'&'
    header="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Noto Sans CJK JP,72,&H00FFFFFF,&H00FFFFFF,&H00122030,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1
Style: Meta,Noto Sans CJK JP,24,&H00C3D9E4,&H00FFFFFF,&H00122030,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Bar,Noto Sans CJK JP,12,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events=[];last=0
    for idx,(a,b,t) in enumerate(cues,1):
        word=KEYWORDS[idx-1]
        if a<last or b<=a or word not in t or any(c in t for c in '{}\\'):raise ValueError('bad cue')
        last=b
        before,after=t.split(word,1)
        body=before+r'{\c'+col+'}'+word+r'{\c&HFFFFFF&}'+after
        start,end=stamp(a),stamp(b)
        events.append(f'Dialogue: 2,{start},{end},Main,,0,0,0,,{{\\pos(474,1462)}}{body}')
        events.append(f'Dialogue: 2,{start},{end},Meta,,0,0,0,,{{\\pos(168,1407)}}VOICE / JP')
        events.append(f'Dialogue: 2,{start},{end},Meta,,0,0,0,,{{\\pos(780,1407)}}{idx:02d} / 16')
        w=round(742*idx/16)
        events.append(f'Dialogue: 2,{start},{end},Bar,,0,0,0,,{{\\pos(103,1533)\\p1\\c{col}}}m 0 0 l {w} 0 {w} 8 0 8{{\\p0}}')
    Path(path).write_text(header+'\n'.join(events)+'\n',encoding='utf-8')
    return len(events)
def render(source,srt,genre,output,config):
    conf=json.loads(Path(config).read_text(encoding='utf-8'))['genres']
    if len(conf)!=10 or len({g['name'] for g in conf})!=10:raise ValueError('need 10 genres')
    accent=next(g['accent'] for g in conf if g['name']==genre)
    output=Path(output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    ass=output.with_suffix('.ass')
    build_ass(read_srt(srt),accent,ass)
    vf=('drawbox=x=0:y=1355:w=1080:h=320:color=0x071828@1:t=fill,'
        'drawbox=x=64:y=1368:w=820:h=184:color=0x0b2a3b@1:t=fill,'
        'drawbox=x=64:y=1368:w=820:h=184:color=0x477f87@1:t=3,'
        'drawbox=x=103:y=1533:w=742:h=8:color=0x214b58@1:t=fill,'
        f'ass={ass},format=yuv420p')
    silent=output.with_name(output.stem+'_silent.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-map','0:v:0','-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(silent)],check=True)
    try:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)],check=True)
    finally:silent.unlink(missing_ok=True)
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ['source','srt','genre','output','config']:p.add_argument('--'+arg,required=True)
    a=p.parse_args()
    print(render(a.source,a.srt,a.genre,a.output,a.config))
