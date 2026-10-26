"""cycle878: genre-neutral Japanese caption safe-area renderer, review only.

Replaces inherited small, low-contrast burned subtitle region with two-line
high-contrast caption cards; does not transcribe, alter or infer audio content.
No media is uploaded to GitHub. All source media must be private review-only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,FRAMES=1080,1920,30,691
TOP,HEIGHT=1450,390
TEXT_LEFT,TEXT_RIGHT=90,865
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}
WINDOWS=((.27,2.93),(3.31,5.60),(5.90,8.23),(8.52,11.10),
         (11.41,13.97),(14.28,16.93),(17.26,19.50),(19.86,23.03))
# Exact visible inherited eight-sentence captions, only reformatted; not ASR.
AI_WORK_LINES=(
 ('AIで仕事を早くするなら、','最初の一歩が大事。'),
 ('まず、繰り返している','作業を書き出そう。'),
 ('次に、完成形の見本を','用意する。'),
 ('指示は、目的と条件を','具体的に伝える。'),
 ('最初の出力は、','必ず自分で確かめる。'),
 ('違いがあれば、修正点を','一つずつ伝える。'),
 ('使える指示は、','テンプレートに残す。'),
 ('小さな時短を、','毎日の習慣にしよう。'),
)

@dataclass(frozen=True)
class CaptionCue:
    start:float
    end:float
    lines:tuple[str,str]

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()

@lru_cache(maxsize=12)
def font(size=64,bold=True):
    return ImageFont.truetype(FONT if bold else FONT_REG,size)

def default_cues():
    return tuple(CaptionCue(s,e,tuple(lines)) for (s,e),lines in zip(WINDOWS,AI_WORK_LINES))

def validate_cues(cues,duration=FRAMES/FPS):
    if not 1<=len(cues)<=16:raise ValueError('1..16 caption cues required')
    previous=0.
    measure=ImageDraw.Draw(Image.new('RGB',(1,1)))
    for cue in cues:
        if not 0<=cue.start<cue.end<=duration+.005 or cue.start<previous-.001:
            raise ValueError('invalid or overlapping caption timing')
        if cue.end-cue.start<.35:raise ValueError('caption too short to read')
        if len(cue.lines)!=2:raise ValueError('exactly two lines required')
        for line in cue.lines:
            if not line or '\n' in line or len(line)>30:raise ValueError('invalid line')
            b=measure.textbbox((0,0),line,font=font())
            if b[2]-b[0]>TEXT_RIGHT-TEXT_LEFT:
                raise ValueError('text exceeds safe width: '+line)
        previous=cue.end
    return True

def cue_at(t,cues):
    return next((i for i,c in enumerate(cues) if c.start<=t<c.end),None)

def make_background():
    im=Image.new('RGBA',(W,HEIGHT));d=ImageDraw.Draw(im)
    for y in range(HEIGHT):
        k=y/HEIGHT
        d.line((0,y,W,y),fill=(4+round(3*k),13+round(5*k),27+round(8*k),255))
    d.line((0,0,W,0),fill=(52,125,148,255),width=3)
    # Edge reserved for TikTok right-side controls; all copy stays left of x=865.
    return im

def make_card(cue,index,total):
    validate_cues((CaptionCue(0.,max(.5,cue.end-cue.start),cue.lines),),duration=24)
    im=Image.new('RGBA',(W,HEIGHT),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((82,30,238,73),radius=15,fill=(18,74,92,255))
    d.text((100,36),'字幕 / '+f'{index+1:02d}',font=font(25),fill=(171,241,246,255))
    d.rounded_rectangle((78,94,88,256),radius=4,fill=(61,217,223,255))
    for y,line in zip((107,197),cue.lines):
        d.text((TEXT_LEFT,y),line,font=font(),fill=(249,252,255,255),
               stroke_width=2,stroke_fill=(0,11,21,255))
    d.rounded_rectangle((86,326,868,334),radius=4,fill=(29,64,81,255))
    d.rounded_rectangle((86,326,86+round(782*(index+1)/total),334),radius=4,
                        fill=(67,214,223,255))
    return im

def build_assets(cues,outdir):
    validate_cues(cues)
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    make_background().save(outdir/'background.png')
    for i,cue in enumerate(cues):make_card(cue,i,len(cues)).save(outdir/f'cue_{i:02d}.png')
    return outdir

def filter_graph(cues,folder=None):
    """Single-stream FFmpeg filter; avoids many infinite looped PNG decoders."""
    if folder is None:folder=Path('/tmp/cycle878_cues')
    folder=Path(folder)
    steps=[
      f'drawbox=x=0:y={TOP}:w=iw:h={HEIGHT}:color=0x071326:t=fill',
      'drawbox=x=78:y=1543:w=10:h=171:color=0x42d5dd:t=fill',
      'drawbox=x=86:y=1780:w=782:h=8:color=0x204354:t=fill',
    ]
    for i,c in enumerate(cues):
        cond=f'gte(t,{c.start})*lt(t,{c.end})'
        for j in range(2):
            name=folder/f'cue_{i:02d}_line{j+1}.txt'
            steps.append(f'drawtext=fontfile={FONT}:textfile={name}:'
                         f'fontcolor=0xf9fcff:fontsize=64:x={TEXT_LEFT}:y={1530+90*j}:'
                         f'borderw=2:bordercolor=0x00111b:enable=\'{cond}\'')
        steps.append(f'drawbox=x=86:y=1780:w={round(782*(i+1)/len(cues))}:'
                     f'h=8:color=0x43d6df:t=fill:enable=\'{cond}\'')
    return ','.join(steps)

def write_textfiles(cues,folder):
    folder=Path(folder)
    for i,c in enumerate(cues):
        for j,line in enumerate(c.lines):
            (folder/f'cue_{i:02d}_line{j+1}.txt').write_text(line,encoding='utf-8')

def render(source,output,manifest,cues=None):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    if output.exists():raise ValueError('refuse overwrite')
    if manifest!={**POLICY,'source_sha256':sha(source)}:
        raise ValueError('fail closed: private source manifest mismatch')
    cues=default_cues() if cues is None else tuple(cues)
    validate_cues(cues)
    with tempfile.TemporaryDirectory(prefix='cycle878_') as td:
        write_textfiles(cues,td)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-vf',filter_graph(cues,td),'-map','0:v:0','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',
             '-r',str(FPS),'-frames:v',str(FRAMES),'-c:a','copy',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=150)
    return {'source_sha256':sha(source),'output_sha256':sha(output),
            'caption_count':len(cues),'caption_safe_x':[TEXT_LEFT,TEXT_RIGHT],
            'caption_safe_y':[TOP,TOP+HEIGHT],'font_px':64,
            'timings_are_editorial_not_asr':True,'speech_semantics_verified':False,
            'policy':POLICY}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','output','manifest','report'):p.add_argument('--'+key,required=True)
    a=p.parse_args()
    result=render(a.source,a.output,json.loads(Path(a.manifest).read_text()))
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))
