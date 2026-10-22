#!/usr/bin/env python3
"""Free/offline, genre-neutral 1080x1920 image slides + timed Japanese subtitles + audio.
This renderer does not post, download assets, synthesize voice or clear media rights.
"""
from pathlib import Path
import argparse, json, re, subprocess

FPS=30
DEFAULT_CUTS=[0,60,120,180,243,282,330,378,429]

def read_cues(path):
    data=Path(path).read_text(encoding='utf-8-sig').strip()
    cues=[]
    for block in re.split(r'\n\s*\n',data):
        match=re.search(r'(\d\d:\d\d:\d\d,\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d,\d\d\d)',block)
        if match: cues.append((match.group(1),match.group(2),block[match.end():].strip().replace('\n',' ')))
    return cues

def secs(t):
    h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)

def ass_time(t):
    h,m,s=t.replace(',','.').split(':');return f'{int(h)}:{m}:{s[:5]}'

def write_ass(cues,path):
    header='''[Script Info]\nTitle: Japanese subtitle safe-area template\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Caption,Noto Sans CJK JP,65,&H00FFFFFF,&H00FFFFFF,&H00112431,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,80,80,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
    for a,b,t in cues:
        assert secs(a)<secs(b),'Nonpositive caption duration'
        clean=t.replace('\\','\\\\').replace('{','').replace('}','')
        header+=f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{{\\pos(540,1585)\\fad(45,45)}}{clean}\n'
    Path(path).write_text(header,encoding='utf-8')

def compose(root,source,output=None,cuts=None):
    root=Path(root).resolve();source=Path(source).resolve()
    cuts=cuts or DEFAULT_CUTS
    assert cuts[0]==0 and len(cuts)>1 and all(b>a for a,b in zip(cuts,cuts[1:])), 'Invalid scene boundaries'
    cues=read_cues(root/'config/phrase_cues.srt')
    assert cues and secs(cues[-1][1])<=cuts[-1]/FPS+.01, 'Caption exceeds video'
    for i in range(len(cuts)-1):
        assert (root/'assets'/f'slide_{i+1:02}.png').exists(),f'Missing slide {i+1}'
    # Explicit frame-aligned durations, no shell quoting or external downloads.
    playlist='ffconcat version 1.0\n'
    for i in range(len(cuts)-1):
        playlist+=f"file '{(root/'assets'/f'slide_{i+1:02}.png')}'\nduration {(cuts[i+1]-cuts[i])/FPS:.9f}\n"
    playlist+=f"file '{(root/'assets'/f'slide_{len(cuts)-1:02}.png')}'\n"
    (root/'config/slides.ffconcat').write_text(playlist)
    ass=root/'config/subtitles.ass';write_ass(cues,ass)
    output=Path(output).resolve() if output else root/'output/cycle771_EDITORIAL_SAFE_HUMAN_REVIEW.mp4'
    output.parent.mkdir(parents=True,exist_ok=True)
    silent=output.with_name(output.stem+'_silent.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-safe','0','-f','concat','-i',str(root/'config/slides.ffconcat'),'-map','0:v:0','-vf',f'fps=30,ass={ass}:fontsdir=/usr/share/fonts/opentype/noto,format=yuv420p','-frames:v',str(cuts[-1]),'-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p',str(silent)]
    subprocess.run(cmd,check=True)
    # Separate remux retains the entire original Japanese AAC stream (no lost final packet).
    remux=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)]
    try: subprocess.run(remux,check=True)
    finally: silent.unlink(missing_ok=True)
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--source',required=True);p.add_argument('--output');args=p.parse_args()
    print(compose(args.root,args.source,args.output))
