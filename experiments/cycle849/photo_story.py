"""Offline, review-only TikTok photo-story renderer (cycle849).

10 genres share one layout. Never uploads, posts, or purchases anything.
Inputs must be rights-cleared by a human before publication.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H, FPS, FRAME_COUNT = 1080, 1920, 30, 691
GENRES = {
    'ai_work': '#32E3D1', 'sales_business': '#FFC96D',
    'beauty': '#E6A7FF', 'romance': '#FF8BAF', 'saving': '#5EE0A5',
    'career': '#FFB67E', 'wellness': '#A7DF77',
    'science': '#7BBEFF', 'travel_food': '#70E0E0',
    'product_comparison_lifestyle': '#FFC0D0'
}
REVIEW_ONLY = {'publication_approved': False, 'automatic_posting': False,
               'rights_confirmed': False, 'employee_approved': False}
SCENES = [
    ('AIで仕事を', 'もっと速く', '最初の一歩を小さくする'),
    ('繰り返す作業を', '見つけよう', '毎日の定型作業を1つ書き出す'),
    ('完成形の見本を', '先に用意', '理想の出力を具体的に見せる'),
    ('目的と条件を', '具体的に伝える', '目的・条件・形式をそろえる'),
    ('AIの回答を', '自分で確認', '数字・日付・根拠をチェック'),
    ('修正点は', '一つずつ', '直すポイントを1つに絞る'),
    ('良い指示は', '保存して再利用', '使えた指示を残しておく'),
    ('小さな時短を', '毎日の習慣に', '明日も1つ、続けてみる'),
]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_REG, size)

def validate(genre, beats, photos):
    if genre not in GENRES or len(GENRES) != 10: raise ValueError('invalid genre')
    if len(photos) != 8 or any(not Path(p).is_file() for p in photos):
        raise ValueError('eight existing source photos required')
    if len(beats) != 24: raise ValueError('24 caption beats required')
    end = 0.0
    for b in beats:
        a, z = float(b['start']), float(b['end'])
        if a < end or z <= a or z > 23.04: raise ValueError('invalid caption timeline')
        end = z
    return True

def make_slide(photo, idx, accent):
    bg = Image.new('RGB', (W,H), '#091728'); d=ImageDraw.Draw(bg)
    d.rounded_rectangle((64,65,326,124), radius=29, fill='#173348')
    d.text((93,77), 'AI  /  WORK', font=font(29), fill=accent)
    d.text((890,75), f'{idx+1:02d} / 08', font=font(29), fill='white')
    for j in range(8):
        d.rounded_rectangle((64+j*121,151,155+j*121,163), radius=6,
                            fill=accent if j<=idx else '#294154')
    title1,title2,action=SCENES[idx]
    d.text((64,222),title1,font=font(73),fill='white',stroke_width=1)
    d.text((64,320),title2,font=font(82),fill=accent,stroke_width=1)
    x0,y0,x1,y1=64,486,1016,1330
    src=Image.open(photo).convert('RGB')
    # Blurred cover fills the card without black bars; the sharp photo is fitted without face cropping.
    cover=ImageOps.fit(src,(x1-x0,y1-y0),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(30))
    bg.paste(cover,(x0,y0))
    sharp=ImageOps.contain(src,(x1-x0-60,y1-y0-185),method=Image.Resampling.LANCZOS)
    bg.paste(sharp,(x0+(x1-x0-sharp.width)//2,y0+30))
    tint=Image.new('RGBA',(x1-x0,y1-y0),(5,15,26,0));td=ImageDraw.Draw(tint)
    for yy in range(420,y1-y0):
        a=int(15+195*(yy-420)/(y1-y0-420))
        td.line((0,yy,x1-x0,yy),fill=(5,13,22,a))
    bg.paste(tint,(x0,y0),tint)
    d=ImageDraw.Draw(bg)
    d.rounded_rectangle((91,512,302,572),radius=22,fill='#0C2435')
    d.text((116,520),f'STEP  {idx+1:02d}',font=font(30),fill=accent)
    d.rounded_rectangle((88,1168,992,1298),radius=26,fill='#0A1C2C')
    d.rectangle((110,1190,118,1275),fill=accent)
    d.text((150,1194),action,font=font(43),fill='white')
    # Reserved caption area is intentionally blank; burned-in timed subtitles are added by ffmpeg.
    d.rounded_rectangle((64,1395,1016,1608),radius=26,fill='#12273A',outline='#3A5867',width=2)
    d.rectangle((85,1433,94,1570),fill=accent)
    d.text((70,1675),'TRY TODAY',font=font(30),fill=accent)
    d.text((70,1740),action,font=font(37),fill='white')
    d.text((70,1850),'HUMAN REVIEW  /  PUBLICATION NOT APPROVED',font=font(19,False),fill='#829AA8')
    return bg

def ass_time(sec):
    cs=round(sec*100);h,cs=divmod(cs,360000);m,cs=divmod(cs,6000);s,cs=divmod(cs,100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'

def make_ass(beats, path):
    header=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Default,Noto Sans CJK JP,72,&H00FFFFFF,&H00FFFFFF,&H00000E19,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,50,50,0,1\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    lines=[]
    for b in beats:
        value=str(b['text']).replace('{','').replace('}','')
        lines.append(f"Dialogue: 0,{ass_time(float(b['start']))},{ass_time(float(b['end']))},Default,,0,0,0,,{{\\an5\\pos(540,1500)}}{value}")
    Path(path).write_text(header+'\n'.join(lines)+'\n',encoding='utf-8')

def render(photos, beats_path, narration_video, output, workdir, genre='ai_work'):
    beats=json.loads(Path(beats_path).read_text(encoding='utf-8'))
    validate(genre,beats,photos)
    workdir=Path(workdir);workdir.mkdir(parents=True,exist_ok=True)
    for i,p in enumerate(photos):make_slide(p,i,GENRES[genre]).save(workdir/f'slide_{i+1:02d}.png')
    make_ass(beats,workdir/'captions.ass')
    # 8 images, 7 x 0.3s dissolves. 691 output frames (23.033s).
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y']
    for i in range(8):
        frames=96 if i==7 else 94
        cmd+=['-loop','1','-framerate','30','-t',str(frames/30),'-i',str(workdir/f'slide_{i+1:02d}.png')]
    cmd+=['-i',str(narration_video)]
    filters=[]
    for i in range(8):
        filters.append(f'[{i}:v]fps=30,format=yuv420p,setsar=1[s{i}]')
    prev='s0'
    for i in range(1,8):
        target=f'x{i}'
        filters.append(f'[{prev}][s{i}]xfade=transition=fade:duration=0.3:offset={i*85/30:.6f}[{target}]')
        prev=target
    ass=str((workdir/'captions.ass').resolve()).replace(':','\\:')
    filters.append(f'[{prev}]ass={ass}[v]')
    cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map','8:a:0',
          '-frames:v',str(FRAME_COUNT),'-c:v','libx264','-preset','veryfast',
          '-crf','20','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return Path(output)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--photos',nargs=8,required=True)
    p.add_argument('--beats',required=True)
    p.add_argument('--narration-video',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--workdir',required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(render(a.photos,a.beats,a.narration_video,a.output,a.workdir,a.genre))
