"""cycle850: reusable, review-only photo-motion renderer for ten genres.

No network calls, posting, paid APIs, or merge operations. 8 input photos must
be rights-reviewed before any employee-approved manual publication.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
if not (Path(__file__).parent / 'photo_story.py').exists():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cycle849'))
import photo_story as base

CARD = (64, 486, 1016, 1330)
CARD_W, CARD_H = CARD[2]-CARD[0], CARD[3]-CARD[1]
ZOOM_MAX = 1.042
GENRES = base.GENRES
REVIEW_ONLY = base.REVIEW_ONLY

def photo_card(photo):
    """Photo-only crop, leaving the typography and labels stationary."""
    source = Image.open(photo).convert('RGB')
    cover = ImageOps.fit(source, (CARD_W, CARD_H), method=Image.Resampling.LANCZOS)
    cover = cover.filter(ImageFilter.GaussianBlur(30))
    sharp = ImageOps.contain(source, (CARD_W-60, CARD_H-185), method=Image.Resampling.LANCZOS)
    cover.paste(sharp, ((CARD_W-sharp.width)//2, 30))
    tint = Image.new('RGBA', (CARD_W,CARD_H), (5,15,26,0))
    d = ImageDraw.Draw(tint)
    for yy in range(420, CARD_H):
        alpha=int(15+195*(yy-420)/(CARD_H-420))
        d.line((0,yy,CARD_W,yy),fill=(5,13,22,alpha))
    cover.paste(tint,(0,0),tint)
    return cover

def foreground(photo, scene_idx, accent):
    """Opaque title and captions outside card; transparent card + static labels."""
    out = base.make_slide(photo, scene_idx, accent).convert('RGBA')
    out.paste((0,0,0,0), CARD)
    d=ImageDraw.Draw(out)
    d.rounded_rectangle((91,512,302,572),radius=22,fill='#0C2435')
    d.text((116,520),f'STEP  {scene_idx+1:02d}',font=base.font(30),fill=accent)
    action=base.SCENES[scene_idx][2]
    d.rounded_rectangle((88,1168,992,1298),radius=26,fill='#0A1C2C')
    d.rectangle((110,1190,118,1275),fill=accent)
    d.text((150,1194),action,font=base.font(43),fill='white')
    return out

def motion_filter(i, frames):
    """Slow center-safe motion. 0.042 zoom avoids large upscaling of small photos."""
    p = f'min(on/{frames-1},1)'
    direction = 1 if i % 2 == 0 else -1
    x = f'(iw-iw/zoom)*(0.5+{direction}*0.12*{p})'
    y = f'(ih-ih/zoom)*(0.5-0.08*{p})'
    z = f'1+{ZOOM_MAX-1:.3f}*{p}'
    return (f'zoompan=z=\'{z}\':x=\'{x}\':y=\'{y}\':'
            f'd=1:s={CARD_W}x{CARD_H}:fps=30')

def validate(photos, beats, genre):
    base.validate(genre, beats, photos)
    assert len(GENRES)==10 and not any(REVIEW_ONLY.values())
    return True

def render(photos, beats_path, narration_video, output, workdir, genre='ai_work'):
    beats=json.loads(Path(beats_path).read_text(encoding='utf-8'))
    validate(photos,beats,genre)
    workdir=Path(workdir);workdir.mkdir(parents=True,exist_ok=True)
    for i,photo in enumerate(photos):
        photo_card(photo).save(workdir/f'card_{i+1:02d}.png')
        foreground(photo,i,GENRES[genre]).save(workdir/f'foreground_{i+1:02d}.png')
    base.make_ass(beats,workdir/'captions.ass')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','2']
    for i in range(8):
        frames=96 if i==7 else 94
        duration=f'{frames/30:.9f}'
        cmd+=['-loop','1','-framerate','30','-t',duration,'-i',str(workdir/f'card_{i+1:02d}.png')]
        cmd+=['-loop','1','-framerate','30','-t',duration,'-i',str(workdir/f'foreground_{i+1:02d}.png')]
    cmd+=['-i',str(narration_video)]
    filters=[]
    for i in range(8):
        frames=96 if i==7 else 94
        filters += [f'[{2*i}:v]{motion_filter(i,frames)},format=rgba,pad=1080:1920:64:486:color=#091728[card{i}]',
                    f'[{2*i+1}:v]format=rgba[fg{i}]',
                    f'[card{i}][fg{i}]overlay=0:0:format=auto:shortest=1,format=yuv420p,setsar=1[s{i}]']
    prev='s0'
    for i in range(1,8):
        filters.append(f'[{prev}][s{i}]xfade=transition=fade:duration=0.3:offset={i*85/30:.6f}[x{i}]')
        prev=f'x{i}'
    ass=str((workdir/'captions.ass').resolve()).replace(':','\\:')
    filters.append(f'[{prev}]ass={ass}[v]')
    cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map','16:a:0',
          '-frames:v','691','-c:v','libx264','-preset','ultrafast','-crf','21',
          '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
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
