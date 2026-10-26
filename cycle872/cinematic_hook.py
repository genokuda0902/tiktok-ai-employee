"""Cycle872: 10-genre cinematic opening with staged synthetic-data proof.

REVIEW ONLY. No third-party uploads, no auto-post, no claim of voice/subtitle semantic sync.
The input MP4/photo are private; only this generic renderer and synthetic tests may be committed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

W, H, FPS, N = 1080, 1920, 30, 691
START, COUNT, TOP, BOTTOM = 0, 89, 132, 1490
CHANGED_END = START + COUNT - 1
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': ('これ、まだ', '手でやってるの？', 'AIで集計を効率化'),
    'sales_business': ('その資料、', 'まだ手作業？', '営業データを整理'),
    'beauty': ('その記録、', '続けられてる？', 'ケアの変化を見える化'),
    'romance': ('その会話、', '振り返れてる？', '大切な言葉を整理'),
    'saving': ('その家計、', '把握できてる？', '支出を見える化'),
    'career': ('その学び、', '活かせてる？', '進捗を見える化'),
    'wellness': ('その習慣、', '記録してる？', '小さな変化を可視化'),
    'science': ('その数字、', '検証してる？', '仮説をデータで確認'),
    'travel_food': ('旅の予定、', '整理できてる？', '予定をひとまとめ'),
    'product_comparison_lifestyle': ('その比較、', '根拠はある？', '選ぶ条件を整理'),
}
POLICY = {
    'review_only': True, 'publication_approved': False,
    'automatic_posting': False, 'external_upload': False,
    'source_rights_reviewed': False, 'synthetic_example_data': True,
}
MONTHS = (('4月', 12, 8), ('5月', 16, 9), ('6月', 18, 12))


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


@lru_cache(maxsize=32)
def font(size):
    return ImageFont.truetype(FONT, size)


def fit(text, width, size):
    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text, font=font(size))
    if bbox[2] - bbox[0] > width:
        raise ValueError('headline clipping risk: ' + text)
    return font(size)


def ease(t):
    t = max(0., min(1., t))
    return t * t * (3 - 2 * t)


def validate(genre, photo, frame):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 0 <= frame < COUNT:
        raise ValueError('frame outside scene')
    if photo.mode not in ('RGB', 'RGBA') or min(photo.size) < 850:
        raise ValueError('photo dimensions/mode rejected')
    a, b, _ = GENRES[genre]
    fit(a, 920, 84)
    fit(b, 930, 91)
    assert sum(row[1] for row in MONTHS) == 46
    assert sum(row[2] for row in MONTHS) == 29


def make_frame(photo, frame, genre='ai_work'):
    """Generate ONLY the safe central band; leave header and caption bands untouched."""
    validate(genre, photo, frame)
    t = frame / (COUNT - 1)
    height = BOTTOM - TOP
    # Reuse a previously generated private original still, crop/zoom distinct from scene 07.
    scale = max(W / photo.width, height / photo.height) * (1.06 + .06 * ease(t))
    nw, nh = math.ceil(photo.width * scale), math.ceil(photo.height * scale)
    bg = ImageEnhance.Color(photo.convert('RGB')).enhance(.86).resize((nw, nh), Image.Resampling.LANCZOS)
    sx, sy = nw - W, nh - height
    cx, cy = round(sx * (.63 - .11 * t)), round(sy * .41)
    bg = bg.crop((cx, cy, cx + W, cy + height)).filter(ImageFilter.GaussianBlur(2.0)).convert('RGBA')
    dark = Image.new('RGBA', (W, height), (3, 15, 31, 0))
    overlay = ImageDraw.Draw(dark, 'RGBA')
    for y in range(height):
        opacity = round(145 + 20 * abs(y / height - .50))
        overlay.line((0, y, W, y), fill=(2, 14, 28, opacity))
    bg = Image.alpha_composite(bg, dark)
    layer = Image.new('RGBA', (W, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, 'RGBA')
    # Visible from first frame: a high-contrast first-1.5-second question.
    d.rounded_rectangle((64, 44, 562, 115), radius=23, fill=(0, 42, 67, 240), outline=(97, 231, 246, 190), width=2)
    d.text((93, 58), 'AI × 仕事術  /  3秒で伝える', font=font(30), fill=(194, 247, 255))
    a, b, sub = GENRES[genre]
    d.text((62, 157), a, font=font(84), fill=(255, 255, 255))
    d.text((62, 264), b, font=font(91), fill=(255, 205, 95))
    d.rounded_rectangle((64, 406, 1018, 1107), radius=30, fill=(5, 20, 37, 240), outline=(104, 209, 237, 220), width=3)
    d.text((99, 440), '月別売上データ  /  架空の例', font=font(39), fill=(244, 250, 255))
    d.rounded_rectangle((94, 515, 987, 601), radius=14, fill=(18, 69, 97, 244))
    for text, x in [('月', 150), ('営業A', 466), ('営業B', 769)]:
        d.text((x, 528), text, font=font(40), fill=(222, 249, 255))
    # Reveal one synthetic row at a time; the real data/UI scene follows next.
    visible_rows = sum(frame >= f for f in (12, 25, 38))
    for i, (month, av, bv) in enumerate(MONTHS):
        y = 630 + i * 112
        d.rounded_rectangle((98, y, 983, y + 98), radius=10,
                            fill=(15 + i * 4, 44 + i * 5, 65 + i * 4, 234))
        for text, x in [(month, 149), (str(av) if i < visible_rows else '—', 480),
                        (str(bv) if i < visible_rows else '—', 787)]:
            d.text((x, y + 19), text, font=font(49),
                   fill=(255, 255, 255) if i < visible_rows else (139, 166, 177))
    if frame < 52:
        d.rounded_rectangle((98, 979, 984, 1086), radius=13, fill=(16, 54, 69, 160))
        d.text((143, 995), '合計', font=font(45), fill=(158, 191, 202))
        d.text((470, 992), '—', font=font(60), fill=(145, 172, 184))
        d.text((770, 992), '—', font=font(60), fill=(145, 172, 184))
    if frame >= 52:
        p = ease((frame - 52) / 12)
        d.rounded_rectangle((98, 979, 984, 1086), radius=13,
                            fill=(3, 92, 113, round(240 * p)), outline=(100, 240, 228, round(240 * p)), width=3)
        d.text((143, 995), '合計', font=font(45), fill=(235, 255, 255, round(255 * p)))
        d.text((470, 992), '46', font=font(60), fill=(255, 232, 145, round(255 * p)))
        d.text((770, 992), '29', font=font(60), fill=(255, 232, 145, round(255 * p)))
    d.rounded_rectangle((65, 1168, 1018, 1292), radius=22, fill=(7, 46, 67, 238), outline=(90, 210, 235, 155), width=2)
    d.text((102, 1197), sub, font=fit(sub, 870, 53), fill=(255, 255, 255))
    # Moving progress accent, outside the subtitle zone.
    d.rounded_rectangle((67, 1320, 1018, 1333), radius=6, fill=(40, 68, 82, 210))
    d.rounded_rectangle((67, 1320, 67 + round(951 * (frame + 1) / COUNT), 1333), radius=6,
                        fill=(77, 226, 241, 255))
    return Image.alpha_composite(bg, layer).convert('RGB')


def probe(path):
    data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))
    v = next(s for s in data['streams'] if s['codec_type'] == 'video')
    a = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    observed = (v['codec_name'], v['width'], v['height'], v['r_frame_rate'], int(v['nb_frames']), a['codec_name'], a['sample_rate'])
    required = ('h264', W, H, '30/1', N, 'aac', '48000')
    if observed != required:
        raise ValueError(f'media mismatch: {observed}')
    return {'resolution': [W, H], 'fps': FPS, 'frames': N, 'seconds': float(data['format']['duration']), 'audio_codec': 'AAC', 'sample_rate': 48000}


def render(source, photo_path, output, manifest, genre='ai_work'):
    source, photo_path, output = map(Path, (source, photo_path, output))
    if output.exists():
        raise ValueError('output exists; refusing overwrite')
    if not source.is_file() or not photo_path.is_file():
        raise ValueError('missing source or private photo')
    expected = {**POLICY, 'source_sha256': sha(source), 'photo_sha256': sha(photo_path)}
    if manifest != expected:
        raise ValueError('review-only source manifest gate failed')
    probe(source)
    with Image.open(photo_path) as x:
        photo = x.copy()
    validate(genre, photo, 0)
    with tempfile.TemporaryDirectory(prefix='cycle872_') as td:
        for i in range(COUNT):
            make_frame(photo, i, genre).save(Path(td) / f'{i:03}.jpg', quality=92, subsampling=0)
        filt = (f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
                f'[0:v][new]overlay=x=0:y={TOP}:enable=\'between(n,{START},{CHANGED_END})\':'
                'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-i', str(source),
               '-framerate', '30', '-i', str(Path(td) / '%03d.jpg'), '-filter_complex', filt,
               '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '20',
               '-pix_fmt', 'yuv420p', '-r', '30', '-frames:v', str(N), '-c:a', 'copy',
               '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True, timeout=300)
    return {'source_sha256': sha(source), 'output_sha256': sha(output), 'changed_frames': COUNT,
            'start': START, 'genres_supported': len(GENRES), 'review_policy': POLICY, 'media': probe(output)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    for name in ('source', 'photo', 'output', 'manifest', 'report'):
        ap.add_argument('--' + name, required=True)
    ap.add_argument('--genre', default='ai_work')
    args = ap.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    report = render(args.source, args.photo, args.output, manifest, args.genre)
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
