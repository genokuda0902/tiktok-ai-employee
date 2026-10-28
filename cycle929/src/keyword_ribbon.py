#!/usr/bin/env python3
"""cycle929: scene-keyword ribbons on a review-only Japanese MP4.
Does not verify speech semantics, approve publishing, or perform posting.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FRAMES = 691
SIZE = (1080, 1920)
RIBBON_SIZE = (354, 110)
RIBBON_XY = (686, 274)
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRE_COLORS = {
    'ai_work': '#2ED7C5', 'finance': '#6BC7FF', 'health': '#8BDFB1',
    'travel': '#A0B9FF', 'beauty': '#F0B5E3', 'cooking': '#FFBD87',
    'education': '#C9B4FF', 'career': '#F2D18E',
    'lifestyle': '#E9B0C9', 'technology': '#8DDDE6',
}
SCENES = (
    (0, 87, '選ぶ'),
    (87, 174, '書き出す'),
    (174, 261, '見本を使う'),
    (261, 348, '目的と条件'),
    (348, 435, '人が確認'),
    (435, 522, '1つずつ修正'),
    (522, 609, '保存する'),
    (609, 691, '今日の1つ'),
)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def scene_for_frame(frame):
    if not 0 <= frame < FRAMES:
        raise ValueError('frame out of range')
    for index, (start, end, word) in enumerate(SCENES, 1):
        if start <= frame < end:
            return index, start, end, word
    raise AssertionError('scene coverage error')

def alpha_for_frame(frame):
    _, start, end, _ = scene_for_frame(frame)
    local = frame - start
    fade_in = min(1.0, local / 11.0)
    fade_out = min(1.0, (end - 1 - frame) / 8.0)
    return max(0.0, min(fade_in, fade_out, 1.0))

def ribbon(frame, genre='ai_work'):
    if genre not in GENRE_COLORS:
        raise ValueError('unsupported genre')
    index, start, end, word = scene_for_frame(frame)
    opacity = alpha_for_frame(frame)
    im = Image.new('RGBA', RIBBON_SIZE, (0, 0, 0, 0))
    if opacity <= 0:
        return im
    d = ImageDraw.Draw(im)
    accent = tuple(bytes.fromhex(GENRE_COLORS[genre][1:]))
    slide = round((1.0 - opacity) * 12)
    left, top, right, bottom = 8 + slide, 8, 344 + slide, 99
    d.rounded_rectangle((left + 3, top + 5, right + 3, bottom + 5),
                        radius=22, fill=(0, 5, 19, 115))
    d.rounded_rectangle((left, top, right, bottom), radius=22,
                        fill=(5, 24, 45, 242), outline=(*accent, 220), width=3)
    d.rounded_rectangle((left + 14, top + 18, left + 68, top + 72),
                        radius=16, fill=(*accent, 230))
    number_font = ImageFont.truetype(FONT_REG, 28) if Path(FONT_REG).exists() else ImageFont.load_default()
    small_font = ImageFont.truetype(FONT_REG, 15) if Path(FONT_REG).exists() else ImageFont.load_default()
    main_font = ImageFont.truetype(FONT, 32) if Path(FONT).exists() else ImageFont.load_default()
    d.text((left + 21, top + 26), f'{index:02d}', font=number_font, fill=(5, 29, 47, 255))
    d.text((left + 85, top + 13), 'KEY POINT', font=small_font, fill=(174, 204, 218, 255))
    d.text((left + 84, top + 37), word, font=main_font, fill=(250, 253, 255, 255))
    if opacity < 1:
        im.putalpha(im.getchannel('A').point(lambda a: round(a * opacity)))
    return im

def render(source, output, genre='ai_work', expected_sha=None):
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if genre not in GENRE_COLORS:
        raise ValueError('unsupported genre')
    if expected_sha and sha256(source) != expected_sha:
        raise RuntimeError('SOURCE_SHA_MISMATCH')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle929_ribbon_') as temp:
        root = Path(temp)
        for frame in range(FRAMES):
            ribbon(frame, genre).save(root / f'ribbon_{frame:04d}.png')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-i', str(source), '-framerate', str(FPS), '-i', str(root / 'ribbon_%04d.png'),
               '-filter_complex', f'[0:v][1:v]overlay={RIBBON_XY[0]}:{RIBBON_XY[1]}:shortest=1:format=auto[v]',
               '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
               '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-frames:v', str(FRAMES),
               '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True, timeout=240)
    return {'cycle': 929, 'source_sha256': sha256(source),
            'output_sha256': sha256(output), 'frames': FRAMES,
            'scenes': len(SCENES), 'genre': genre, 'policy': POLICY}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', choices=list(GENRE_COLORS), default='ai_work')
    p.add_argument('--expected-source-sha')
    p.add_argument('--report')
    args = p.parse_args()
    result = render(args.source, args.output, args.genre, args.expected_source_sha)
    if args.report:
        Path(args.report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
