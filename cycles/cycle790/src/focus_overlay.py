"""cycle790: scene-aware animated focus highlights on original 8-slide Japanese video.

No external images, voice generation, paid API or posting. Input must be an approved
review-source MP4 with existing Japanese narration and subtitles. Audio is copied.
ASS vector annotations are restricted to the central illustration panel; caption
region and platform UI safety margins are not touched.
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

FPS=30
FRAMES=(60,60,60,64,39,48,48,50)
W,H=1080,1920
FOCUS_BOXES=((383,782,672,1080),(352,735,575,994),(674,703,968,1110),
             (126,638,965,830),(580,922,732,1094),(117,857,970,1064),
             (132,787,904,948),(380,697,708,1042))
GENRE_COLORS={
 'ai_work':'35E8D2','beauty':'F0A5D8','relationships':'FF98B9',
 'saving':'79D7FF','sales_business':'FFD176','career':'77E2C4',
 'health':'77DBBD','science':'35E8D2','travel_food':'FFA877',
 'product_lifestyle':'A8CFFF'}

def ass_time(frames: int)->str:
    cs=round(frames*100/FPS)
    h,cs=divmod(cs,360000); m,cs=divmod(cs,6000); s,cs=divmod(cs,100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'

def ass_color(rgb: str)->str:
    return '&H00'+rgb[4:6]+rgb[2:4]+rgb[0:2]

def validate_boxes(boxes=FOCUS_BOXES):
    if len(boxes)!=len(FRAMES): raise ValueError('Expected 8 focus boxes')
    for left,top,right,bottom in boxes:
        if not (90<=left<right<=985 and 560<=top<bottom<=1380):
            raise ValueError('Focus must stay within artwork safe area')

def create_ass(path: str|Path,genre='science')->Path:
    validate_boxes()
    if genre not in GENRE_COLORS: raise ValueError('Unknown genre')
    color=ass_color(GENRE_COLORS[genre])
    header='''[Script Info]
Title: cycle790 focus pulse
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Focus,Noto Sans CJK JP,30,&H00FFFFFF,&H00FFFFFF,&H0035E8D2,&H00000000,-1,0,0,0,100,100,0,0,1,5,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    start=0
    for frames,(l,t,r,b) in zip(FRAMES,FOCUS_BOXES):
        end=start+frames
        for width,alpha in ((15,'B8'),(5,'00')):
            pathshape=f'm {l} {t} l {r} {t} {r} {b} {l} {b}'
            tag=(r'{\an7\pos(0,0)\p1\1a&HFF&\3a&H'+alpha+
                 r'&\3c'+color+r'\bord'+str(width)+
                 r'\shad0\fad(180,180)\t(150,650,\bord'+str(width+2)+r')}' )
            header+=f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Focus,,0,0,0,,{tag}{pathshape}\n'
        start=end
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(header,encoding='utf-8');return p

def render(input_mp4:str|Path,output_mp4:str|Path,work:str|Path,genre='science'):
    src=Path(input_mp4); dst=Path(output_mp4)
    if not src.is_file():raise FileNotFoundError(src)
    if src.resolve()==dst.resolve():raise ValueError('Input and output must differ')
    dst.parent.mkdir(parents=True,exist_ok=True)
    ass=create_ass(Path(work)/'focus.ass',genre)
    video_only=Path(work)/'video_only.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
         '-i',str(src),'-vf',f'ass={ass}', '-map','0:v:0','-an',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-r','30','-frames:v',str(sum(FRAMES)),str(video_only)]
    subprocess.run(cmd,check=True)
    mux=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
         '-i',str(video_only),'-i',str(src),'-map','0:v:0','-map','1:a:0',
         '-c','copy','-movflags','+faststart',
         '-metadata','comment=HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',str(dst)]
    subprocess.run(mux,check=True)
    return dst

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    p.add_argument('--work',required=True);p.add_argument('--genre',default='science',choices=sorted(GENRE_COLORS))
    a=p.parse_args();render(a.input,a.output,a.work,a.genre)
