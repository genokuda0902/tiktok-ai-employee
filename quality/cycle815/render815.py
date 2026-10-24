"""cycle815: 24-state Japanese caption emphasis, FFmpeg/libass, no posting.

Inputs: previous approved-for-internal-review MP4 and voice_timing.json.
Three-way caption timing is an estimate, not word-level forced alignment.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
OUT.mkdir(exist_ok=True)
GENRE_ACCENTS={
    'ai_work':'#77d5ff','beauty':'#ffa2c3','love_psychology':'#c3a0ff',
    'money_saving':'#ffd475','sales_business':'#61f0c7','career':'#84b9ff',
    'health_life':'#b4e97d','science':'#86d9ff','travel_food':'#ffbb8b',
    'product_life':'#d7b0ff'}
PHRASES=[
 ['仕事ができる人は、','質問が','違う。'],
 ['まず、','目指すゴールを','確認する。'],
 ['次に、','今の数字を','確かめる。'],
 ['そして、','理想との差を','一つに絞る。'],
 ['原因には、','なぜを','三回重ねる。'],
 ['対策は、','今日できる','行動に変える。'],
 ['結果を見て、','また','修正する。'],
 ['小さな改善が、','強いチームを','つくる。']]

def ass_time(seconds):
    cs=round(seconds*100)
    return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def make_ass(timing_path:Path,dest:Path):
    timing=json.loads(timing_path.read_text(encoding='utf-8'))
    durations=[s['seconds'] for s in timing['sentences']]
    assert len(durations)==len(PHRASES)==8
    assert all(''.join(p)==s['text'] for p,s in zip(PHRASES,timing['sentences']))
    ends=[0];total=0
    for seconds in durations:
        total+=seconds
        ends.append(round(total*30))
    ends[-1]=775
    head="""[Script Info]
Title: cycle815 Japanese three-state captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,65,&H00FFFBF7,&H00FFFBF7,&H00132328,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,8,65,65,0,1
Style: Label,Noto Sans CJK JP,29,&H00C7F061,&H00C7F061,&H00132328,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,8,65,65,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events=[]
    gold='&H0067CEFF&'
    white='&H00FFFBF7&'
    for scene,p in enumerate(PHRASES):
        start,end=ends[scene],ends[scene+1]
        cuts=[start,round(start+(end-start)/3),round(start+2*(end-start)/3),end]
        for phase in range(3):
            s,e=cuts[phase],cuts[phase+1]
            if e<=s:raise ValueError('zero-length caption state')
            colored=[]
            for j,part in enumerate(p):
                c=gold if j==phase else white
                colored.append(r'{\c'+c+'}'+part)
            cap=r'{\an8\pos(540,1450)}'+colored[0]+r'\N'+colored[1]+colored[2]
            label=rf'{{\an8\pos(540,1384)}}字幕強調　{scene+1:02d} / 08　・　{phase+1} / 3'
            events.append(f'Dialogue: 0,{ass_time(s/30)},{ass_time(e/30)},Caption,,0,0,0,,{cap}')
            events.append(f'Dialogue: 1,{ass_time(s/30)},{ass_time(e/30)},Label,,0,0,0,,{label}')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(head+'\n'.join(events)+'\n',encoding='utf-8')
    return ends

def render(source:Path,timing:Path,target:Path):
    ass=OUT/'karaoke815.ass'
    ends=make_ass(timing,ass)
    filt=(f'drawbox=x=71:y=1352:w=938:h=277:color=0x061625:t=fill,'
          f'drawbox=x=71:y=1352:w=938:h=277:color=0x3a7a84:t=3,'
          f'ass={ass}:shaping=complex,format=yuv420p')
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
         '-vf',filt,'-map','0:v:0','-map','0:a:0','-c:v','libx264',
         '-preset','veryfast','-crf','18','-threads','2','-c:a','copy',
         '-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True)
    return ends

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--timing',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    render(Path(a.input),Path(a.timing),Path(a.output))
