#!/usr/bin/env python3
"""cycle753: cinematic, truthful prompt-typing visualization (review-only).

A synthetic UI animation, NOT a recording of ChatGPT or an AI-generated result.
All displayed values are invented. The previous Japanese narration and lower-third
subtitles are preserved verbatim; never publish without employee review.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 540, 960, 30
START, END = 6.5, 9.8
FRAMES = round((END - START) * FPS)
VALUES = (120000, 150000, 200000, 180000)
PROMPT_LINES = (
    'この売上データを',
    '月別に集計して、',
    '棒グラフ用の表と',
    '合計を出してください。',
)
GENRE_COLORS = {
    'ai_work': (65, 228, 215), 'romance': (255, 143, 191),
    'beauty': (224, 157, 239), 'money': (151, 224, 139),
    'trivia': (255, 207, 113), 'gadgets': (123, 190, 255),
    'health': (107, 218, 164), 'sales': (255, 169, 109),
    'travel': (113, 210, 237), 'mystery': (188, 165, 255),
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SAFE = (26, 45, 425, 582)
REGIONS = {
    'heading': (32, 55, 419, 185),
    'window': (32, 215, 420, 505),
    'footnote': (32, 518, 420, 580),
}

def validate():
    if len(GENRE_COLORS) != 10 or len(set(GENRE_COLORS)) != 10:
        raise ValueError('10 distinct genres required')
    if sum(VALUES) != 650000 or any(type(v) is not int or v <= 0 for v in VALUES):
        raise ValueError('synthetic data inconsistency')
    if not PROMPT_LINES or any(len(line) > 15 for line in PROMPT_LINES):
        raise ValueError('prompt line too long')
    a, b, c, d = SAFE
    for name, (x0, y0, x1, y1) in REGIONS.items():
        if not (a <= x0 < x1 <= c and b <= y0 < y1 <= d):
            raise ValueError('unsafe visual region: ' + name)
    return True

def font(sz, bold=True):
    return ImageFont.truetype(FONT if bold else REGULAR, sz)

def clamp(t):
    return max(0.0, min(1.0, t))

def smooth(t):
    t = clamp(t)
    return t*t*(3-2*t)

def shown_lines(progress):
    """Text reveal is monotonic and never fabricates a response."""
    all_text = '\n'.join(PROMPT_LINES)
    count = min(len(all_text), int(clamp(progress)*len(all_text)))
    return all_text[:count].split('\n')

def frame_at(index: int, genre: str = 'ai_work') -> Image.Image:
    validate()
    if genre not in GENRE_COLORS:
        raise ValueError('unknown genre')
    if not 0 <= index < FRAMES:
        raise ValueError('frame out of bounds')
    accent = GENRE_COLORS[genre]
    seconds = index/FPS
    base = Image.new('RGBA', (W, 605), (3, 15, 29, 255))
    draw = ImageDraw.Draw(base)
    for y in range(605):
        draw.line((0, y, W, y), fill=(5+int(y*.017), 18+int(y*.024), 32+int(y*.032), 255))
    light = Image.new('RGBA', (W, 605), (0,0,0,0))
    ld = ImageDraw.Draw(light)
    ld.ellipse((50 + round(17*math.sin(seconds*1.5)), 65, 565, 515), fill=(*accent, 47))
    ld.ellipse((-140, 205, 220, 680), fill=(20, 114, 203, 50))
    base = Image.alpha_composite(base, light.filter(ImageFilter.GaussianBlur(72)))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((32, 56, 419, 92), radius=9, fill=(13, 54, 64), outline=accent, width=2)
    draw.text((45, 60), 'AI時短ラボ  /  STEP 02', font=font(19), fill='white')
    draw.text((32, 116), 'AIに伝えるのは', font=font(35), fill='white')
    draw.text((32, 160), 'たった4行の指示', font=font(27), fill=accent)
    draw.rounded_rectangle((40, 224, 429, 512), radius=19, fill=(0, 0, 0, 150))
    draw.rounded_rectangle((32, 215, 420, 505), radius=20, fill=(12, 32, 48), outline=accent, width=3)
    draw.rounded_rectangle((45, 229, 407, 268), radius=10, fill=(17, 56, 70))
    draw.text((58, 236), '入力デモ  /  架空データ', font=font(19), fill='white')
    draw.rounded_rectangle((45, 280, 407, 327), radius=11, fill=(19, 87, 86), outline=(77, 202, 191), width=1)
    draw.text((59, 291), '▣  売上データ_架空.csv   •   4か月', font=font(17), fill='white')
    draw.rounded_rectangle((45, 338, 407, 460), radius=13, fill=(237, 248, 250), outline=(175, 208, 214), width=2)
    progress = smooth((seconds - 0.20) / 2.68)
    lines = shown_lines(progress)
    for j, line in enumerate(lines[:4]):
        draw.text((60, 346 + j*26), line, font=font(20, False), fill=(14, 41, 55))
    if index % 20 < 13 and progress < 0.99:
        current = lines[-1] if lines else ''
        x = 60 + int(draw.textlength(current, font=font(20, False)))
        y = 350 + (len(lines)-1)*26
        draw.rounded_rectangle((x+2, y, x+5, y+21), radius=1, fill=accent)
    enabled = progress > .985
    draw.rounded_rectangle((279, 467, 406, 494), radius=10,
                           fill=(*accent, 255) if enabled else (51, 102, 124), width=1)
    draw.text((298, 469), '送信（例）', font=font(16), fill=(4, 31, 39) if enabled else 'white')
    draw.text((49, 472), f'指示入力  {int(progress*100):>3}%', font=font(16), fill=(192, 218, 224))
    draw.rounded_rectangle((32, 520, 420, 558), radius=10, fill=(9, 40, 57), outline=accent, width=2)
    draw.text((44, 525), '実演ではなく、操作手順の再現です', font=font(17), fill='white')
    draw.text((32, 563), '※架空データ／実際のAI操作映像ではありません', font=font(13, False), fill=(189, 212, 220))
    mask = Image.new('L', (W, 605), 255)
    md = ImageDraw.Draw(mask)
    for y in range(596, 605):
        md.line((0, y, W, y), fill=round(255*(605-y)/9))
    base.putalpha(mask)
    out = Image.new('RGBA', (W, H), (0,0,0,0))
    out.alpha_composite(base)
    return out

def make_frames(folder: Path, genre: str):
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(FRAMES):
        frame_at(i, genre).save(folder / f'overlay_{i:03d}.png')

def render(source: Path, folder: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    filter_graph = (
        f'[1:v]format=rgba,scale=1080:1920:flags=lanczos,'
        f'setpts=PTS-STARTPTS+{START}/TB[scene];'
        '[0:v][scene]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]'
    )
    cmd = ['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
           '-i',str(source),'-framerate',str(FPS),'-i',str(folder/'overlay_%03d.png'),
           '-filter_complex',filter_graph,'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
           '-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd, check=True, timeout=240)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--genre', choices=sorted(GENRE_COLORS), default='ai_work')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='cycle753_') as folder:
        make_frames(Path(folder), args.genre)
        render(args.source, Path(folder), args.output)
if __name__ == '__main__':
    main()
