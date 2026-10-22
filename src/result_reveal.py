#!/usr/bin/env python3
"""cycle775: image-first chart result reveal, zero-budget and review-only.

A deterministic, genre-agnostic visual renderer. All figures are synthetic.
Inherited source audio is NOT licensed or voice-to-subtitle aligned by this code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle775_chart_contract import validate_contract

WIDTH, HEIGHT, FPS, TOTAL_FRAMES = 1080, 1920, 30, 819
START, END = 300, 384  # 10.0s to 12.8s, exclusive
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRE_COLORS = {
    'AI・仕事効率化': '#20C7BB', '美容・身だしなみ': '#E774A8',
    '恋愛・心理': '#F18AAB', 'お金・節約': '#D5A72C',
    '営業・ビジネス': '#4688DD', '転職・キャリア': '#9B76D5',
    '健康・生活改善': '#4AAE7D', '雑学・科学': '#419CC9',
    '旅行・グルメ': '#DE8E48', '商品比較・暮らし': '#8E78C5',
}
DATA = [('1月', 120000), ('2月', 150000), ('3月', 200000), ('4月', 180000)]


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def validate(manifest, source):
    validate_contract(manifest)
    if manifest['source_sha256'] != digest(source):
        raise ValueError('input hash mismatch')
    if manifest['genre'] not in GENRE_COLORS or set(manifest['supported_genres']) != set(GENRE_COLORS):
        raise ValueError('ten genre configuration required')
    if manifest['monthly_sales'] != dict(DATA) or manifest['total_yen'] != sum(v for _, v in DATA):
        raise ValueError('synthetic source and total mismatch')
    if manifest.get('asset_provenance') != 'original_vector_only':
        raise ValueError('unapproved third-party image prohibited')
    if manifest.get('audio_rights') != 'unverified_review_only':
        raise ValueError('inherited audio is not approved')
    if manifest.get('quality_approved') is not False or manifest.get('review_status') != 'HUMAN_REVIEW':
        raise ValueError('quality must be human reviewed')
    if manifest.get('publish_mode') != 'employee_manual_after_approval':
        raise ValueError('no automatic posting')
    if manifest.get('time_saved_claim') is not None:
        raise ValueError('time-saving claims require evidence')
    if not Path(FONT).exists():
        raise ValueError('Japanese font unavailable')
    return True


@lru_cache(maxsize=20)
def font(size):
    return ImageFont.truetype(FONT, size)


def hex_rgb(h):
    return tuple(bytes.fromhex(h.lstrip('#')))


def clamp(v):
    return max(0.0, min(1.0, v))


def smooth(v):
    x = clamp(v)
    return x*x*(3-2*x)


def chart_layout():
    return [(160, '1月', 120000), (365, '2月', 150000),
            (570, '3月', 200000), (775, '4月', 180000)]


def draw_static(accent):
    c = hex_rgb(accent)
    im = Image.new('RGB', (WIDTH, HEIGHT), (9, 22, 42))
    d = ImageDraw.Draw(im)
    for y in range(0, HEIGHT, 5):
        f = y / HEIGHT
        d.rectangle((0, y, WIDTH, y+5), fill=(int(8+6*f), int(23+10*f), int(44+14*f)))
    # Soft original vector glow, never sourced from external media.
    glow = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-230, 250, 760, 1230), fill=(*c, 43))
    gd.ellipse((650, 800, 1320, 1580), fill=(61, 141, 255, 33))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    im = Image.alpha_composite(im.convert('RGBA'), glow)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((70, 153, 477, 223), radius=19,
                        fill=(5, 52, 66, 255), outline=(*c, 235), width=3)
    d.text((96, 167), 'AI時短ラボ  /  RESULT', font=font(29), fill=(241, 255, 255, 255))
    d.text((76, 288), '売上の全体像が、', font=font(62), fill=(244, 250, 255, 255))
    d.text((76, 384), 'ひと目でわかる。', font=font(68), fill=(*c, 255))
    d.text((78, 492), '架空の4か月分の売上をグラフで比較', font=font(31), fill=(199, 218, 229, 255))
    # A large, bright reference-inspired chart; contrast and label size matter on phones.
    d.rounded_rectangle((70, 605, 1010, 1500), radius=39,
                        fill=(246, 250, 253, 255), outline=(220, 236, 241, 255), width=4)
    d.text((112, 655), '月別売上', font=font(52), fill=(22, 53, 67, 255))
    d.text((812, 673), '単位：万円', font=font(27), fill=(79, 110, 121, 255))
    for value, yy in [(0, 1335), (10, 1145), (20, 955)]:
        d.line((127, yy, 964, yy), fill=(201, 215, 223, 255), width=2)
        d.text((101, yy-20), str(value), font=font(25), fill=(84, 112, 123, 255))
    d.line((127, 1335, 964, 1335), fill=(80, 120, 138, 255), width=3)
    # Static labels, moving bars and numbers are overlaid in draw_frame.
    for x, month, _ in chart_layout():
        d.text((x+30, 1381), month, font=font(41), fill=(26, 60, 72, 255))
    d.rounded_rectangle((70, 1543, 1010, 1690), radius=27,
                        fill=(12, 51, 68, 245), outline=(*c, 255), width=3)
    d.text((110, 1574), '4か月合計', font=font(38), fill=(218, 241, 247, 255))
    d.text((78, 1742), '操作の再現イメージ  /  架空データ', font=font(30), fill=(190, 216, 225, 255))
    d.text((78, 1822), '※ 結果は実演データ・時短効果は未測定', font=font(25), fill=(168, 193, 204, 255))
    return im.convert('RGB')


def draw_frame(base, idx, genre):
    if genre not in GENRE_COLORS or not (0 <= idx < END-START):
        raise ValueError('invalid frame or genre')
    c = hex_rgb(GENRE_COLORS[genre])
    im = base.copy()
    d = ImageDraw.Draw(im)
    t = idx / FPS
    for j, (x, month, amount) in enumerate(chart_layout()):
        # Staggered bar reveal, all numbers are source-verified.
        progress = smooth((t - (0.20 + j*0.38))/0.72)
        h = round((amount / 200000) * 381 * progress)
        if h > 0:
            y = 1335-h
            color = c if j == 3 else (48, 166, 206)
            d.rounded_rectangle((x, y, x+123, 1335), radius=15, fill=color)
        if progress > .96:
            d.text((x-2, 1335-round((amount/200000)*381)-65),
                   f'{amount//10000}万', font=font(41), fill=(27, 65, 78))
    if t >= 2.08:
        p = smooth((t-2.08)/.5)
        if p > .03:
            d.text((430, 1567), '650,000円', font=font(58), fill=(*c, round(255*p)))
    else:
        d.text((430, 1567), 'グラフを作成中…', font=font(36), fill=(199, 227, 232))
    return im


def run(cmd):
    subprocess.run(cmd, check=True)


def render(source, manifest_path, output, frames_dir, smoke=False):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    validate(manifest, source)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)
    n = 12 if smoke else END-START
    base = draw_static(GENRE_COLORS[manifest['genre']])
    edges = []
    if not smoke:
        for name, seconds in [('start', START/FPS), ('end', (END-1)/FPS)]:
            path = frames_dir.parent / f'{name}_edge.jpg'
            run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(seconds), '-i', str(source),
                 '-frames:v', '1', str(path)])
            edges.append(Image.open(path).convert('RGB'))
    for i in range(n):
        frame = draw_frame(base, i, manifest['genre'])
        if not smoke:
            if i < 8:
                # A directional wipe avoids the double-exposed Japanese text
                # caused by crossfading two information-dense scenes.
                cut = round(WIDTH*smooth((i+1)/8))
                wipe = edges[0].copy()
                wipe.paste(frame.crop((0, 0, cut, HEIGHT)), (WIDTH-cut, 0))
                frame = wipe
            elif i >= n-8:
                shift = round(WIDTH*smooth((i-(n-8)+1)/8))
                wipe = edges[1].copy()
                if shift < WIDTH:
                    wipe.paste(frame.crop((shift, 0, WIDTH, HEIGHT)), (0, 0))
                frame = wipe
        frame.save(frames_dir / f'{i:04d}.jpg', quality=90, subsampling=0)
    if smoke:
        run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(FPS),
             '-i', str(frames_dir/'%04d.jpg'), '-c:v', 'libx264',
             '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', str(output)])
    else:
        tmp = output.parent / 'temporary_noaudio.mp4'
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(source), '-itsoffset', str(START/FPS),
             '-framerate', str(FPS), '-i', str(frames_dir/'%04d.jpg'),
             '-filter_complex', '[0:v][1:v]overlay=eof_action=pass:shortest=0:format=auto,format=yuv420p[v]',
             '-map', '[v]', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '20',
             '-an', '-r', str(FPS), '-frames:v', str(TOTAL_FRAMES),
             '-movflags', '+faststart', str(tmp)])
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-i', str(source),
             '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'copy',
             '-movflags', '+faststart', str(output)])
        tmp.unlink()
    return {'output': str(output), 'sha256': digest(output), 'frames_rendered': n,
            'approved_for_publication': False}


def main():
    p = argparse.ArgumentParser()
    for key in ('source', 'manifest', 'output', 'frames_dir'):
        p.add_argument('--'+key.replace('_','-'), type=Path, required=True)
    p.add_argument('--smoke', action='store_true')
    args = p.parse_args()
    print(json.dumps(render(args.source, args.manifest, args.output, args.frames_dir, args.smoke), ensure_ascii=False))


if __name__ == '__main__':
    main()
