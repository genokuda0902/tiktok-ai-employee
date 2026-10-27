"""Offline 10-genre 1080x1920 focus guides; review only, no ASR or posting."""
from dataclasses import dataclass
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
GENRES = ('AI時短','雑学','料理','美容','お金','健康','旅行','商品','ストーリー','仕事術')
SAFE_CONTENT = (60, 300, 870, 1190)

@dataclass(frozen=True)
class Focus:
    start: float
    end: float
    x: int
    y: int
    w: int
    h: int
    label: str
    accent: str = 'cyan'

# Editorial timing based on reviewed local demo and subtitles, NOT word-level ASR.
FOCUSES = (
    Focus(8.70, 9.65, 200, 708, 660, 84, '目的欄'),
    Focus(9.65, 11.05, 200, 794, 660, 86, '条件欄'),
    Focus(11.55, 12.65, 95, 672, 765, 155, '出力例'),
    Focus(12.65, 14.24, 95, 868, 765, 310, '人間による確認'),
    Focus(14.42, 15.26, 111, 519, 725, 261, '曖昧な指示', 'amber'),
    Focus(15.26, 16.99, 111, 815, 725, 324, '具体的な指示'),
    Focus(17.32, 18.27, 202, 710, 655, 82, '保存名'),
    Focus(18.27, 19.61, 106, 795, 752, 190, '保存内容'),
)

def validate(focuses=FOCUSES, duration=23.033333):
    if len(GENRES)!=10 or len(set(GENRES))!=10:
        raise ValueError('ten unique genres required')
    left,top,right,bottom=SAFE_CONTENT
    previous_end=0.0
    for f in focuses:
        if not 0<=f.start<f.end<=duration: raise ValueError('invalid timing')
        if f.start<previous_end-1e-8: raise ValueError('overlap')
        if not (left<=f.x<f.x+f.w<=right and top<=f.y<f.y+f.h<=bottom):
            raise ValueError('unsafe focus geometry')
        if f.w<90 or f.h<60: raise ValueError('focus too small')
        if f.accent not in ('cyan','amber'): raise ValueError('invalid accent')
        previous_end=f.end
    return True

def timestamp(t):
    total=int(round(t*100))
    h,rem=divmod(total,360000);m,rem=divmod(rem,6000);s,cs=divmod(rem,100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'

def rect(x,y,w,h):
    return f'm {x} {y} l {x+w} {y} {x+w} {y+h} {x} {y+h}'

def corners(f,thickness=8,length=52):
    x,y,w,h=f.x,f.y,f.w,f.h
    r=[(x,y,length,thickness),(x,y,thickness,length),
       (x+w-length,y,length,thickness),(x+w-thickness,y,thickness,length),
       (x,y+h-thickness,length,thickness),(x,y+h-length,thickness,length),
       (x+w-length,y+h-thickness,length,thickness),(x+w-thickness,y+h-length,thickness,length)]
    return ' '.join(rect(*a) for a in r)

def write_ass(destination,focuses=FOCUSES,duration=23.033333):
    validate(focuses,duration)
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    header='''[Script Info]
Title: cycle888 review-only editorial focus
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Guide,DejaVu Sans,24,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines=[header]
    for f in focuses:
        color='&HE1DA26&' if f.accent=='cyan' else '&H35C6FF&'
        fade=min(170,int((f.end-f.start)*1000/4))
        tag=r'{\an7\pos(0,0)\p1\bord0\shad0\c'+color+rf'\fad({fade},{fade})'+'}'
        lines.append(f'Dialogue: 0,{timestamp(f.start)},{timestamp(f.end)},Guide,,0,0,0,,{tag}{corners(f)}\n')
    destination.write_text(''.join(lines),encoding='utf-8')
    return destination
