"""Cycle959: review-only mobile-readable Japanese subtitle panel renderer.

Creates a frame-accurate RGBA overlay for a reviewed 8-scene image slideshow.
Only reviewed source hash + genre can render; no publishing or rights assertions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA = 'd57c2224d64c9d589caadbbb0fe487507becc403b2d4e74f1c41d8bef80e632a'
FRAMES = 691
CUTS = (0, 87, 174, 261, 348, 435, 522, 609, 691)
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PANEL_W, PANEL_H, PANEL_Y = 1080, 270, 1450
# 10-genre reusable color configurations. Only ai_work source is currently reviewed.
GENRE_ACCENTS = {
    'ai_work': '#57E2D3', 'business': '#70B7FF', 'finance': '#F2D17A',
    'education': '#F5B96B', 'career': '#99C4FF', 'wellness': '#A7E1B0',
    'lifestyle': '#F0B4D1', 'technology': '#79D4E8', 'travel': '#FFCC8D',
    'trivia': '#C8ACFF',
}
# Exact existing subtitle text transcribed from eight source frames; no new claim.
SCENES = (
    ((('AIで仕事', True), ('を早くするなら、', False)), (('最初の一歩が大事。', False),)),
    ((('まず、', False), ('繰り返している作業を', True)), (('書き出す。', False),)),
    ((('次に、', False), ('完成形の見本を', True)), (('用意する。', False),)),
    ((('指示は、', False), ('目的と条件を', True)), (('具体的', True), ('に伝える。', False))),
    ((('最初の出力は、', False),), (('必ず自分で', True), ('確かめる。', False))),
    ((('違いがあれば、', False), ('修正点を', True)), (('一つずつ', True), ('伝える。', False))),
    ((('使える指示は、', False),), (('テンプレートに', True), ('残す。', False))),
    ((('小さな時短を、', False),), (('毎日の習慣に', True), ('しよう。', False))),
)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def scene_at_frame(frame: int) -> int:
    if not 0 <= frame < FRAMES:
        raise ValueError('frame out of range')
    return next(i for i in range(8) if CUTS[i] <= frame < CUTS[i + 1])

def font_for_line(draw: ImageDraw.ImageDraw, line, max_px: int = 68):
    for px in range(max_px, 49, -1):
        font = ImageFont.truetype(FONT_PATH, px, index=0)
        total = sum(draw.textlength(t, font=font) for t, _ in line)
        if total <= 912:
            return font, px, total
    raise ValueError('line too long for mobile-safe width')

def panel_for_scene(scene: int, genre: str = 'ai_work') -> tuple[Image.Image, dict]:
    if genre not in GENRE_ACCENTS:
        raise ValueError('unknown genre')
    if not 0 <= scene < 8:
        raise ValueError('unknown scene')
    im = Image.new('RGBA', (PANEL_W, PANEL_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((32, 4, 1048, 258), radius=32, fill=(4, 11, 29, 255), outline=(59, 88, 118, 255), width=3)
    d.rounded_rectangle((49, 30, 58, 230), radius=5, fill=GENRE_ACCENTS[genre])
    sizes, bounds = [], []
    for line_index, line in enumerate(SCENES[scene]):
        font, size, width = font_for_line(d, line)
        sizes.append(size)
        x = (PANEL_W - width) / 2
        y = 47 if line_index == 0 else 139
        for text, emphasized in line:
            color = '#FFE365' if emphasized else '#F6F9FF'
            d.text((x, y), text, font=font, fill=color, stroke_width=1, stroke_fill='#162034')
            w = d.textlength(text, font=font)
            bounds.append((x, y, x + w, y + size))
            x += w
    assert all(70 <= b[0] and b[2] <= 1010 for b in bounds)
    return im, {'scene': scene + 1, 'font_sizes_px': sizes, 'text_bounds': bounds}

def build_overlays(folder: Path, genre: str = 'ai_work') -> list[dict]:
    folder.mkdir(parents=True, exist_ok=True)
    meta = []
    for i in range(8):
        im, details = panel_for_scene(i, genre)
        im.save(folder / f'scene_{i + 1:02}.png')
        meta.append(details)
    for frame in range(FRAMES):
        link = folder / f'overlay_{frame + 1:04}.png'
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(f'scene_{scene_at_frame(frame) + 1:02}.png')
    return meta

def render(source: Path, output: Path, genre: str = 'ai_work') -> dict:
    if genre != 'ai_work' or sha256(source) != SOURCE_SHA:
        raise PermissionError('unreviewed source or genre: fail closed')
    output.parent.mkdir(parents=True, exist_ok=True)
    folder = output.parent / 'overlay_frames'
    metrics = build_overlays(folder, genre)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-i', str(source), '-framerate', '30', '-start_number', '1',
           '-i', str(folder / 'overlay_%04d.png'),
           '-filter_complex', f'[0:v][1:v]overlay=x=0:y={PANEL_Y}:format=auto:shortest=1[v]',
           '-map', '[v]', '-map', '0:a:0', '-frames:v', str(FRAMES),
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
           '-pix_fmt', 'yuv420p', '-c:a', 'copy',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
           '-metadata:s:a:0', 'language=jpn', '-movflags', '+faststart', str(output)]
    subprocess.run(cmd, check=True, timeout=240)
    return {'source_sha256': sha256(source), 'output_sha256': sha256(output),
            'output': str(output), 'scene_count': 8, 'frames': FRAMES,
            'subtitle_panel_y': PANEL_Y, 'text_metrics': metrics,
            'genre': genre, 'publication_approved': False, 'command': cmd}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--genre', default='ai_work')
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output, a.genre), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
