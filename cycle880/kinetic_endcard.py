"""cycle880: genre-neutral, review-only kinetic end card for a private MP4.

Only the upper 1340 px are replaced. Original narration, audio bitstream,
Japanese sentence subtitles and lower audio-reactive meter remain untouched.
This is an original reimplementation, not the recovered v33 generator.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile

FPS = 30
W, H = 1080, 1920
CARD_H = 1340
START_FRAME = 588  # 19.600 s, final scene begins
TOTAL_FRAMES = 691
SAFE_CAPTION_Y = 1450
REVIEW_POLICY = {'review_only': True, 'publication_approved': False,
                 'external_upload': False, 'automatic_posting': False,
                 'source_rights_reviewed': False}

@dataclass(frozen=True)
class EndCard:
    genre: str
    headline: str
    subhead: str
    steps: tuple[str, str, str]
    details: tuple[str, str, str]
    cta: str

GENRES = ('ai_work','money','career','learning','health_general','travel',
          'food','beauty_general','home','technology')

DEFAULT = EndCard('ai_work', '今日の5分を、取り戻す', '次の作業で、1つだけ試す',
                  ('元データを用意', '目的と条件を伝える', '数字を自分で確認'),
                  ('4〜6月の架空売上表', '整理 → 集計 → 照合', '営業A 46 / 営業B 29'),
                  '保存して、次の作業で試す')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def validate_story(story: EndCard):
    if story.genre not in GENRES: raise ValueError('unknown genre')
    if len(story.steps) != 3 or len(story.details) != 3:
        raise ValueError('exactly 3 steps/details required')
    for val, limit in ((story.headline, 21), (story.subhead, 28), (story.cta, 25)):
        if not val or len(val) > limit: raise ValueError('invalid copy length')
    for val in (*story.steps, *story.details):
        if not val or len(val) > 30: raise ValueError('invalid step copy')
    all_text = ''.join((story.headline, story.subhead, *story.steps, *story.details, story.cta))
    if any(x in all_text for x in ('@', 'http://', 'https://', 'LINE ID', '電話番号')):
        raise ValueError('unsafe public identifier or URL')
    return True


def validate_manifest(source: Path, manifest: dict):
    expected = {**REVIEW_POLICY, 'source_sha256': sha256(source)}
    if manifest != expected: raise ValueError('fail closed: unapproved or mismatched source')
    return True


def eased(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1-x)**3


def stage_progress(frame):
    """Frame-relative reveal values, suitable for all ten genre storyboards."""
    if not 0 <= frame < TOTAL_FRAMES - START_FRAME: raise ValueError('bad frame')
    t = frame / FPS
    return tuple(eased((t - start)/.42) for start in (.18, .74, 1.30)), eased((t-1.90)/.52)


@lru_cache(maxsize=1)
def base_background():
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.new('RGB',(W,CARD_H))
    d = ImageDraw.Draw(im)
    for y in range(CARD_H):
        d.line((0,y,W,y),fill=(7,20+int(y/CARD_H*7),37+int(y/CARD_H*9)))
    glow=Image.new('RGBA',(W,CARD_H),(0,0,0,0))
    g=ImageDraw.Draw(glow)
    g.ellipse((430,-310,1420,780),fill=(29,141,180,105))
    glow=glow.filter(ImageFilter.GaussianBlur(180))
    return Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB')


def frame_image(frame: int, story: EndCard):
    from PIL import ImageDraw, ImageFont
    validate_story(story)
    levels, cta_level = stage_progress(frame)
    im = base_background().copy()
    d = ImageDraw.Draw(im)
    font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    bold = lambda n: ImageFont.truetype(font, n)
    reg = lambda n: ImageFont.truetype(regular, n)
    d.rounded_rectangle((58,38,340,100),radius=26,fill=(8,62,74),outline=(40,138,154),width=2)
    d.text((86,48),'AI WORK  /  08',font=bold(30),fill=(219,249,255))
    d.text((866,49),'08 / 08',font=bold(29),fill=(105,226,236))
    d.rounded_rectangle((58,136,1022,390),radius=30,fill=(9,33,52),outline=(47,132,157),width=3)
    d.text((92,171),story.headline,font=bold(66),fill=(243,251,255),stroke_width=1,stroke_fill=(8,30,50))
    d.text((95,291),story.subhead,font=reg(38),fill=(111,224,234))
    d.rounded_rectangle((60,422,1020,1130),radius=30,fill=(9,25,42),outline=(26,84,111),width=2)
    for i,alpha in enumerate(levels):
        y=450+i*220
        dy=round((1-alpha)*55)
        bg=(17+round(8*alpha), 46+round(10*alpha), 65+round(12*alpha))
        d.rounded_rectangle((87,y+dy,993,y+dy+186),radius=24,fill=bg,outline=(41,150,166) if alpha>.2 else (25,64,81),width=3)
        d.rounded_rectangle((114,y+dy+35,212,y+dy+135),radius=22,fill=(12,118,137))
        d.text((130,y+dy+53),f'{i+1:02d}',font=bold(40),fill=(242,255,255))
        if alpha > .05:
            d.text((245,y+dy+21),story.steps[i],font=bold(49),fill=(242,253,255))
            d.text((248,y+dy+103),story.details[i],font=reg(32),fill=(157,216,226))
    if cta_level > .01:
        y=1161+round((1-cta_level)*45)
        d.rounded_rectangle((65,y,1015,y+132),radius=29,fill=(24,152,169),outline=(112,244,240),width=3)
        d.text((111,y+28),story.cta,font=bold(45),fill=(255,255,255))
        d.text((936,y+35),'›',font=bold(56),fill=(255,255,255))
    return im


def render(source, output, manifest, story=DEFAULT):
    source,output=Path(source),Path(output)
    if not source.is_file() or output.exists(): raise ValueError('source missing or output exists')
    validate_story(story)
    validate_manifest(source,manifest)
    with tempfile.TemporaryDirectory(prefix='cycle880_') as tmp:
        folder=Path(tmp)
        for f in range(TOTAL_FRAMES-START_FRAME):
            frame_image(f,story).save(folder/f'card_{f:04d}.png',compress_level=3)
        # Overlay starts precisely at 19.600s. The 580-pixel lower subtitle band
        # is never overwritten. Audio is stream-copied (no resynthesis).
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
             '-i',str(source),'-itsoffset',str(START_FRAME/FPS),
             '-framerate',str(FPS),'-i',str(folder/'card_%04d.png'),
             '-filter_complex','[0:v][1:v]overlay=x=0:y=0:shortest=0:eof_action=pass:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),
             '-frames:v',str(TOTAL_FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=300)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'changed_scene_start_frame':START_FRAME,'total_frames':TOTAL_FRAMES,
            'caption_safe_y':SAFE_CAPTION_Y,'genre':story.genre,
            'narration_semantics_verified':False,'source_rights_verified':False,
            'policy':REVIEW_POLICY}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    result=render(a.source,a.output,m)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
