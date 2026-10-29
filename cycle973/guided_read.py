#!/usr/bin/env python3
"""Cycle973: reusable, review-only Japanese reading-focus overlay for image-slide MP4s.

No remote services, no auto posting, no paid assets. Source audio is stream-copied.
Only 10 explicit genre palettes are permitted; unknown genres fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SCENE_BOUNDS = (5.82, 8.67)
ROW_RECTS = ((151, 657, 885, 799), (151, 811, 885, 956), (151, 963, 885, 1112))
CAPTION_TOP = 1320
GENRE_PALETTES = {
    'ai_work': '#14c7c5', 'finance': '#f0ba52', 'learning': '#5baceb',
    'health': '#65cda4', 'travel': '#ed9f5e', 'food': '#e4a66c',
    'science': '#9e94ec', 'history': '#b8a27d', 'business': '#51c4de',
    'lifestyle': '#dd98c4',
}
LABELS = ('成果', '気づき', '次の行動')
FONT_CANDIDATES = (
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
)

def font(size):
    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def rgb(hexcolor):
    return tuple(int(hexcolor[i:i+2], 16) for i in (1,3,5))

def validate(genre, rows=ROW_RECTS, bounds=SCENE_BOUNDS):
    if genre not in GENRE_PALETTES:
        raise ValueError(f'Unreviewed genre: {genre}')
    if len(rows) != 3 or not (0 <= bounds[0] < bounds[1]):
        raise ValueError('Invalid rows or time window')
    for x1,y1,x2,y2 in rows:
        if not (0 <= x1 < x2 <= W and 0 <= y1 < y2 < CAPTION_TOP):
            raise ValueError('Row would cover the caption safe area')
    return True

def create_overlay(genre, index, path, rows=ROW_RECTS):
    validate(genre, rows)
    if index not in (0,1,2):
        raise ValueError('Index must be 0, 1 or 2')
    accent = rgb(GENRE_PALETTES[genre]); x1,y1,x2,y2 = rows[index]
    im = Image.new('RGBA', (W,H), (0,0,0,0))
    glow = Image.new('RGBA',(W,H),(0,0,0,0)); gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((x1-5,y1-5,x2+5,y2+5),radius=25,outline=(*accent,150),width=11)
    im = Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(im)
    if index != 1:  # The source slide already highlights row 2; avoid a double border.
        d.rounded_rectangle((x1-5,y1-5,x2+5,y2+5),radius=23,outline=(*accent,235),width=6)
    for j, (_,ry1,_,ry2) in enumerate(rows):
        cy=(ry1+ry2)//2
        d.ellipse((102,cy-11,124,cy+11),fill=(*accent,245) if j==index else (95,118,129,140))
    d.rounded_rectangle((679,385,903,446),radius=19,fill=(7,32,42,236))
    d.ellipse((695,405,713,423),fill=(*accent,255))
    d.text((726,398),f'{index+1}/3 {LABELS[index]}',font=font(23),fill=(255,255,255,255))
    if im.getbbox() and im.getbbox()[3] >= CAPTION_TOP:
        raise ValueError('Overlay overlaps caption region')
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    im.save(path)
    return path

def render(source,output,genre='ai_work',synthetic=False,crf=19):
    validate(genre)
    source=Path(source); output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    assets=output.parent/'overlay_assets'; assets.mkdir(exist_ok=True)
    overlays=[create_overlay(genre,i,assets/f'focus_{i+1}.png') for i in range(3)]
    times=((0.15,1.00),(1.00,1.85),(1.85,2.80)) if synthetic else ((5.82,6.73),(6.73,7.64),(7.64,8.66))
    chain=[]; previous='[0:v]'
    for i,(a,b) in enumerate(times):
        dest=f'[v{i+1}]'
        chain.append(f"{previous}[{i+1}:v]overlay=x=0:y=0:enable='between(t,{a},{b})':format=auto{dest}")
        previous=dest
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
    for path in overlays: cmd+=['-loop','1','-framerate','30','-i',str(path)]
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(source)]))
    source_frames=int(probe['streams'][0]['nb_read_frames'])
    cmd+=['-filter_complex',';'.join(chain),'-map',previous,'-map','0:a:0',
          '-c:v','libx264','-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p',
          '-r','30','-frames:v',str(source_frames),'-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work',choices=list(GENRE_PALETTES))
    p.add_argument('--synthetic',action='store_true');p.add_argument('--report')
    a=p.parse_args(); result=render(a.source,a.output,a.genre,a.synthetic)
    report={'output':str(result),'sha256':sha(result),'genre':a.genre,
            'synthetic':a.synthetic,'scene03_guided_read':list(LABELS),
            'publication_approved':False,'independent_asr':'NOT_RUN'}
    if a.report:Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
