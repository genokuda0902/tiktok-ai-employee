"""cycle876 — deterministic source-to-prompt scene for ten genres (review only).

Reimplementation, NOT the original v33 renderer.  The browser-like UI is a
local illustration, not a live ChatGPT/Excel screen or a real AI response.
Private inherited MP4/audio never leave the local runtime or enter GitHub.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from cycle874.chart_truth import GENRES, validate_genre

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, COUNT, TOP, BOTTOM = 251, 85, 285, 1450
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
POLICY = {'review_only': True, 'publication_approved': False,
          'external_upload': False, 'automatic_posting': False,
          'source_rights_reviewed': False}
PROMPT_LINES = (
    'この3期間の架空データを整理',
    '2項目の合計とグラフを作成',
    '最後に元データと照合して',
)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


@lru_cache(maxsize=64)
def font(size, bold=True):
    return ImageFont.truetype(FONT if bold else REGULAR, size)


def source_record(genre):
    g = validate_genre(genre)
    rows = tuple((p, a, b) for p, a, b in zip(g.period, g.a, g.b))
    return {'genre': genre, 'headline': g.headline, 'labels': (g.label_a, g.label_b),
            'rows': rows, 'totals': (sum(g.a), sum(g.b))}


def prompt(genre):
    source_record(genre)
    return '\n'.join(PROMPT_LINES)


def safe_text(draw, xy, value, maxwidth, size, fill, bold=True):
    f = font(size, bold)
    bbox = draw.textbbox((0, 0), value, font=f)
    if bbox[2] - bbox[0] > maxwidth:
        raise ValueError('text would clip: ' + value)
    draw.text(xy, value, font=f, fill=fill)


@lru_cache(maxsize=1)
def background():
    im = Image.new('RGB', (WIDTH, BOTTOM - TOP))
    d = ImageDraw.Draw(im)
    for y in range(BOTTOM - TOP):
        k = y / (BOTTOM - TOP)
        d.line((0, y, WIDTH, y), fill=(8 + int(7*k), 20 + int(21*k), 38 + int(23*k)))
    return im


def typed_lines(i):
    # 0-8f: data preview; 9-51f: three lines typed; 52-84f: inspect result.
    chars = max(0, min(sum(map(len, PROMPT_LINES)), (i - 8) * 2))
    result = []
    for line in PROMPT_LINES:
        result.append(line[:max(0, min(len(line), chars))])
        chars -= len(line)
    return tuple(result)


def frame(i, genre='ai_work'):
    if not 0 <= i < COUNT:
        raise ValueError('frame outside target scene')
    s = source_record(genre)
    im = background().copy()
    d = ImageDraw.Draw(im, 'RGBA')
    cyan = (84, 228, 238)
    white = (242, 250, 255)
    muted = (166, 202, 220)
    # Clearly distinguish a simulated demo from real ChatGPT/Excel operation.
    d.rounded_rectangle((56, 22, 495, 86), radius=23,
                        fill=(14, 72, 90, 255), outline=cyan, width=2)
    safe_text(d, (79, 38), 'OFFLINE DEMO  /  架空データ', 415, 25, white)
    safe_text(d, (55, 122), '元データを見せてから指示する', 972, 48, white)
    safe_text(d, (57, 196), '入力 → 指示 → 検算  ／  ローカル再現映像', 970, 33, muted, False)

    # Data preview: all numbers come from cycle874's ten-genre shared source.
    d.rounded_rectangle((56, 274, 1024, 531), radius=24,
                        fill=(13, 37, 59, 255), outline=(62, 145, 174), width=3)
    safe_text(d, (82, 291), s['headline'], 880, 38, white)
    safe_text(d, (91, 354), f"{s['labels'][0]}  /  {s['labels'][1]}", 840, 33, muted)
    for j, (period, a, b) in enumerate(s['rows']):
        x = 86 + j * 310
        d.rounded_rectangle((x, 409, x+283, 492), radius=15,
                            fill=(18, 71, 88, 255), outline=(51, 129, 151), width=2)
        safe_text(d, (x+13, 425), f'{period}   {a} / {b}', 260, 32, white)

    # A source-driven prompt appears as a real typing animation, not a claim
    # that a cloud service was called. Avoid platform logos/brand impersonation.
    d.rounded_rectangle((56, 564, 1024, 977), radius=24,
                        fill=(13, 37, 56, 255), outline=(73, 153, 178), width=3)
    d.rounded_rectangle((56, 564, 1024, 634), radius=22,
                        fill=(22, 65, 84, 255))
    d.rectangle((56, 609, 1024, 634), fill=(22, 65, 84, 255))
    d.ellipse((81, 587, 97, 603), fill=(255, 177, 110))
    d.ellipse((113, 587, 129, 603), fill=(90, 221, 201))
    safe_text(d, (159, 580), '指示入力  |  ローカル操作見本', 795, 33, white)
    d.rounded_rectangle((82, 656, 995, 862), radius=18,
                        fill=(235, 247, 251, 255))
    typed = typed_lines(i)
    for j, line in enumerate(typed):
        if line:
            safe_text(d, (111, 678 + 61*j), line, 830, 39, (18, 45, 63), False)
    if i < 55 and (i // 7) % 2 == 0:
        # Cursor at the end of the last typed line, within the safe input area.
        j = max((j for j, line in enumerate(typed) if line), default=0)
        line = typed[j]
        width = d.textbbox((0, 0), line, font=font(39, False))[2]
        d.rectangle((114 + width, 688 + 61*j, 119 + width, 730 + 61*j), fill=(25, 92, 119))
    d.rounded_rectangle((734, 881, 991, 949), radius=20,
                        fill=(35, 143, 168, 255) if i >= 51 else (36, 87, 110, 255))
    safe_text(d, (777, 897), '送信（デモ）', 208, 31, white)
    if 52 <= i < 66:
        d.rounded_rectangle((725, 878, 1000, 952), radius=22,
                            outline=(249, 209, 93), width=5)

    # Deterministic result, computed from the same values as the displayed input.
    d.rounded_rectangle((57, 1000, 1023, 1116), radius=23,
                        fill=(13, 62, 79, 255), outline=(65, 177, 196), width=2)
    if i < 52:
        msg = '入力内容を確認してから実行'
    elif i < 67:
        msg = '指示と元データを照合中（演出）'
    else:
        msg = f"合計見本  {s['labels'][0]} {s['totals'][0]}  /  {s['labels'][1]} {s['totals'][1]}"
    safe_text(d, (88, 1035), msg, 900, 39, white)
    return im


def render(source, output, manifest, genre='ai_work'):
    source, output = Path(source), Path(output)
    if output.exists():
        raise ValueError('refuse to overwrite review media')
    if not source.is_file():
        raise FileNotFoundError('missing local review source')
    if manifest != {**POLICY, 'source_sha256': sha(source)}:
        raise ValueError('fail-closed manifest: no public permission')
    evidence = source_record(genre)
    with tempfile.TemporaryDirectory(prefix='cycle876_') as td:
        for i in range(COUNT):
            frame(i, genre).save(Path(td) / f'{i:03d}.png')
        filt = (f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/({FPS}*TB)[overlay];'
                f'[0:v][overlay]overlay=x=0:y={TOP}:enable=\'between(n,{START},{START+COUNT-1})\':'
                'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin',
               '-i', str(source), '-framerate', str(FPS),
               '-i', str(Path(td)/'%03d.png'), '-filter_complex', filt,
               '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264',
               '-preset', 'ultrafast', '-crf', '20', '-pix_fmt', 'yuv420p',
               '-r', str(FPS), '-frames:v', str(FRAMES), '-c:a', 'copy',
               '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True, timeout=300)
    return {'source_sha256': sha(source), 'output_sha256': sha(output),
            'start_frame': START, 'changed_frames': COUNT,
            'source_data': evidence, 'ten_genres_supported': len(GENRES),
            'ui_is_synthetic': True, 'policy': POLICY}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    for name in ('source', 'output', 'manifest', 'report'):
        ap.add_argument('--' + name, required=True)
    ap.add_argument('--genre', default='ai_work')
    args = ap.parse_args()
    report = render(args.source, args.output,
                    json.loads(Path(args.manifest).read_text()), args.genre)
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))