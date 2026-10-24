#!/usr/bin/env python3
"""Cycle803 original CTA card. Only use locally approved media for full render.

Generic across ten genres. Public CI renders only synthetic visual+440Hz tone.
Inherited audio/video are NEVER included in GitHub or Actions artifacts.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善', '雑学・科学',
    '旅行・グルメ', '商品比較・暮らし',
)
PALETTES = {
    'AI・仕事効率化': ('#2CE6F2', '#FF2D8A'),
    '美容・身だしなみ': ('#FFC7F0', '#E33B9D'),
    '恋愛・心理': ('#FFB7D3', '#FF5580'),
    'お金・節約': ('#FFD85B', '#2AB48C'),
    '営業・ビジネス': ('#66BFFF', '#FFB94B'),
    '転職・キャリア': ('#9BDAFF', '#FFAC64'),
    '健康・生活改善': ('#85E4B2', '#54B3E8'),
    '雑学・科学': ('#A6B2FF', '#FFAB59'),
    '旅行・グルメ': ('#FFC982', '#FF7899'),
    '商品比較・暮らし': ('#A7E6E4', '#FBAA65'),
}
SAFE = {'left': 160, 'right': 170, 'top': 140, 'bottom': 270}
FPS = 30
CTA_START = 20.8
CTA_END = 23.8


def _font_path():
    choices = [
        os.environ.get('CYCLE803_FONT', ''),
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf',
    ]
    for p in choices:
        if p and Path(p).is_file():
            return p
    raise RuntimeError('Japanese Noto CJK font missing; install fonts-noto-cjk (free)')


def _font(size):
    return ImageFont.truetype(_font_path(), size)


def _rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))


def _mix(a, b, f):
    return tuple(round(a[i]*(1-f)+b[i]*f) for i in range(3))


def _center_text(draw, y, text, font, fill, *, shadow=False):
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = (1080-width)//2
    if x < SAFE['left'] or x+width > 1080-SAFE['right']:
        raise ValueError(f'text outside TikTok safe zone: {text} x={x} width={width}')
    if shadow:
        draw.text((x+3, y+5), text, font=font, fill=(0, 0, 0, 175), stroke_width=3, stroke_fill=(0,0,0,160))
    draw.text((x, y), text, font=font, fill=fill)
    return x, x+width


def _rounded_gradient(w, h, top, bottom, radius):
    image = Image.new('RGBA', (w, h))
    d = ImageDraw.Draw(image)
    for y in range(h):
        f = y / max(1, h-1)
        d.line((0, y, w, y), fill=_mix(top, bottom, f)+(255,))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1), radius=radius, fill=255)
    image.putalpha(mask)
    return image


def _background():
    im = Image.new('RGB', (1080, 1920))
    px = im.load()
    # One-time per render. Non-licensed, mathematically generated light field.
    for y in range(1920):
        for x in range(1080):
            a = math.exp(-((x-740)**2/(580**2)+(y-770)**2/(610**2)))
            b = math.exp(-((x-260)**2/(500**2)+(y-1520)**2/(450**2)))
            px[x,y] = (int(3+5*a+9*b), int(12+39*a+8*b), int(29+62*a+40*b))
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    d = ImageDraw.Draw(layer)
    # Reproducible bokeh field, no external image rights.
    for k in range(65):
        x=(k*187+99)%1180-50
        y=(k*311+71)%1510+40
        r=5+(k*13)%26
        c=(30, 180, 255, 65) if k%3 else (252, 154, 78, 48)
        d.ellipse((x-r,y-r,x+r,y+r), fill=c)
    layer=layer.filter(ImageFilter.GaussianBlur(21))
    im=Image.alpha_composite(im.convert('RGBA'), layer)
    d=ImageDraw.Draw(im)
    for y in range(160,1640,190):
        d.line((125,y,955,y), fill=(70,164,199,20), width=2)
    return im


def _robot(accent):
    # Original layered illustration: glossy shell, illuminated visor, hand wave.
    im = Image.new('RGBA', (780,850), (0,0,0,0))
    d=ImageDraw.Draw(im)
    # Outer cyan glow + soft cast shadow.
    glow=Image.new('RGBA',im.size)
    gd=ImageDraw.Draw(glow)
    gd.rounded_rectangle((100,98,704,648), radius=235, fill=accent+(110,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(56)))
    shadow=Image.new('RGBA',im.size)
    sd=ImageDraw.Draw(shadow)
    sd.ellipse((160,630,700,780), fill=(0,0,0,180))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(42)))
    d=ImageDraw.Draw(im)
    # Shoulder and body
    d.rounded_rectangle((260,558,622,819), radius=142, fill=(184,211,230,255), outline=(239,250,255,255), width=8)
    d.rounded_rectangle((300,608,575,790), radius=94, fill=(33,69,103,255))
    d.rounded_rectangle((366,650,524,740), radius=35, fill=(4,29,54,255), outline=accent+(255,), width=7)
    d.text((406,664), 'AI', font=_font(52), fill=(235,252,255,255))
    # Animated-like waving arm to left of helmet
    d.rounded_rectangle((130,420,235,690), radius=52, fill=(211,232,246,255), outline=(255,255,255,255), width=7)
    d.ellipse((92,355,265,525), fill=(236,246,255,255), outline=(116,173,212,255), width=13)
    d.rounded_rectangle((102,245,151,425), radius=25, fill=(245,250,255,255))
    d.rounded_rectangle((163,200,212,405), radius=25, fill=(245,250,255,255))
    d.rounded_rectangle((225,240,270,415), radius=22, fill=(225,240,255,255))
    # Shell layered shading.
    d.rounded_rectangle((210,80,704,602), radius=195, fill=(88,138,187,255))
    for j in range(24):
        f=j/24
        col=_mix((252,253,255),(131,179,211),f)
        d.rounded_rectangle((216+j//2,87+j//2,694-j//2,590-j//2), radius=192, outline=col+(255,), width=4)
    d.rounded_rectangle((228,95,684,570), radius=182, fill=(223,242,255,255), outline=(255,255,255,255), width=10)
    d.ellipse((265,103,596,182), fill=(255,255,255,190))
    # Visor black glass
    d.rounded_rectangle((260,205,662,509), radius=114, fill=(1,9,32,255), outline=(81,162,216,255), width=8)
    d.arc((278,209,634,334), 187, 344, fill=(153,221,255,180), width=18)
    d.ellipse((330,330,400,419), fill=accent+(255,))
    d.ellipse((511,330,581,419), fill=accent+(255,))
    d.ellipse((345,337,359,355), fill=(255,255,255,255))
    d.ellipse((526,337,540,355), fill=(255,255,255,255))
    d.rounded_rectangle((220,279,262,418), radius=22, fill=(255,255,255,255))
    return im


def make_base(genre):
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    accent, pink = [_rgb(c) for c in PALETTES[genre]]
    im=_background()
    # A bright centered 3D-like robot rather than a cropped flat illustration.
    robot=_robot(accent)
    im.alpha_composite(robot,(146,390))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((171,165,909,234),radius=30,fill=(9,34,60,245),outline=accent+(255,),width=3)
    _center_text(d,177,'AI時短ラボ  /  SAVE',_font(38),(224,246,255,255))
    _center_text(d,265,'次は、あなたの番。',_font(65),(255,255,255,255),shadow=True)
    _center_text(d,350,'3ステップで、あとから再現。',_font(39),(174,229,248,255))
    # Three readable chips in TikTok-safe horizontal bounds.
    chips=['① 表を用意','② AIに指示','③ 結果を確認']
    for i,chip in enumerate(chips):
        x=175+i*250
        d.rounded_rectangle((x,1245,x+232,1335),radius=24,fill=(8,45,70,242),outline=accent+(255,),width=3)
        bb=d.textbbox((0,0),chip,font=_font(29));tw=bb[2]-bb[0]
        d.text((x+(232-tw)//2,1266),chip,font=_font(29),fill=(255,255,255,255))
    # Main CTA button with double stroke and generous padding.
    d.rounded_rectangle((172,1390,908,1545),radius=47,fill=(255,246,255,255))
    d.rounded_rectangle((181,1399,899,1536),radius=39,fill=pink+(255,))
    _center_text(d,1420,'保存して、あとで試そう',_font(53),(255,255,255,255),shadow=True)
    _center_text(d,1600,'※架空データ・操作イメージ｜公開未承認',_font(26),(169,196,215,255))
    return im


def frame(base, t, genre):
    if not 0 <= t <= CTA_END-CTA_START+1e-6:
        raise ValueError('time out of CTA range')
    im=base.copy()
    d=ImageDraw.Draw(im)
    accent=_rgb(PALETTES[genre][0])
    # A non-obstructive moving scan highlight around CTA (30fps, 3 seconds).
    wave=0.5+0.5*math.sin(t*math.tau*1.15)
    alpha=int(70+110*wave)
    d.rounded_rectangle((173,1391,907,1544),radius=46,outline=accent+(alpha,),width=6)
    # Glint travels along the top edge, while no text moves or gets cropped.
    x=205+int(650*(t/3))
    d.ellipse((x-9,1383,x+9,1401),fill=(255,255,255,215))
    return im.convert('RGB')


def render_frames(out_dir, genre, fps=FPS, seconds=3.0):
    if fps != 30 or not (0.5 <= seconds <= 3.0):
        raise ValueError('Unsupported timing')
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    base=make_base(genre)
    for i in range(round(fps*seconds)):
        frame(base,i/fps,genre).save(out/f'{i:04d}.png',compress_level=1)
    return out


def run(cmd):
    subprocess.run(cmd,check=True)


def build(source, output, frames, ffmpeg='ffmpeg'):
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    # Only last 90 frames replaced; input audio packet stream-copied, no new TTS claims.
    run([ffmpeg,'-hide_banner','-loglevel','error','-y',
         '-i',str(source),'-framerate','30','-i',str(Path(frames)/'%04d.png'),
         '-filter_complex',f'[1:v]setpts=PTS+{CTA_START}/TB[cta];[0:v][cta]overlay=x=0:y=0:enable=gte(t\\,{CTA_START}):eof_action=pass:repeatlast=0:shortest=0[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast',
         '-crf','23','-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output)])


def synthetic(output, frames, ffmpeg='ffmpeg'):
    # A 3.0-second original-video CI proof with electronic test tone ONLY.
    run([ffmpeg,'-hide_banner','-loglevel','error','-y','-framerate','30',
         '-i',str(Path(frames)/'%04d.png'),'-f','lavfi','-i','sine=frequency=440:duration=3:sample_rate=48000',
         '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
         '-r','30','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(output)])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--genre',default='AI・仕事効率化',choices=GENRES)
    p.add_argument('--frames',required=True)
    p.add_argument('--source-video')
    p.add_argument('--output',required=True)
    p.add_argument('--synthetic-tone-ci',action='store_true')
    p.add_argument('--review-only',action='store_true')
    p.add_argument('--ffmpeg',default='ffmpeg')
    a=p.parse_args()
    if a.synthetic_tone_ci == bool(a.source_video):
        p.error('Exactly one of --source-video or --synthetic-tone-ci required')
    if not a.review_only:
        p.error('Fail-closed: --review-only is mandatory; never publish automatically')
    frames=render_frames(a.frames,a.genre)
    if a.synthetic_tone_ci:
        synthetic(a.output,frames,a.ffmpeg)
    else:
        build(a.source_video,a.output,frames,a.ffmpeg)
    print(json.dumps({'output':a.output,'review_only':True,'genre':a.genre,'synthetic_tone_ci':a.synthetic_tone_ci},ensure_ascii=False))

if __name__=='__main__':
    main()
