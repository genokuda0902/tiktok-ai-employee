#!/usr/bin/env python3
"""Cycle1116: show legible fictional-data / human-review provenance in scene06.

Review-only reimplementation, not the original v33 renderer. Source is SHA-pinned;
no private assets are uploaded. The existing Japanese AAC stream is copied intact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRE_ACCENTS = {
    'ai': '#67e3d5', 'business': '#83d9ff', 'money': '#f4db86',
    'learning': '#a0d8ff', 'health': '#8de6c7', 'food': '#ffd29b',
    'travel': '#90e6ed', 'beauty': '#ffbddb', 'career': '#a4caff',
    'life': '#c9e6a4',
}
CANVAS = (1080, 1920)
BANNER = (48, 1075, 1032, 1215)
CAPTION_START = 1280
EDIT = (14.3, 17.333333)
BG = '#061827'
WHITE = '#ffffff'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def run(args, binary=False):
    p = subprocess.run(args, check=True, capture_output=True, text=not binary)
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def audio_sha(path):
    b = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-'], binary=True)
    return hashlib.sha256(b).hexdigest()


def luminance(h):
    vals = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in vals]
    return .2126*v[0] + .7152*v[1] + .0722*v[2]


def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)), reverse=True)
    return (x + .05) / (y + .05)


def validate_config(genre):
    if genre not in GENRE_ACCENTS:
        raise ValueError('unknown genre; fail closed')
    if BANNER[3] >= CAPTION_START:
        raise ValueError('would overlap Japanese captions')
    if contrast(GENRE_ACCENTS[genre], BG) < 7:
        raise ValueError('insufficient accent contrast')
    if contrast(WHITE, BG) < 7:
        raise ValueError('insufficient body contrast')
    return genre


def make_overlay(path, genre):
    validate_config(genre)
    im = Image.new('RGBA', CANVAS, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    accent = GENRE_ACCENTS[genre]
    d.rounded_rectangle(BANNER, radius=22, fill=BG, outline=accent, width=4)
    d.rounded_rectangle((70, 1093, 84, 1195), radius=5, fill=accent)
    main = '架空データ｜数値は人が確認'
    note = '社内レビュー用・公開／投稿は未承認'
    f1 = ImageFont.truetype(FONT, 43)
    f2 = ImageFont.truetype(FONT_REG, 30)
    assert d.textbbox((0, 0), main, font=f1)[2] < 895
    assert d.textbbox((0, 0), note, font=f2)[2] < 895
    d.text((106, 1088), main, font=f1, fill=WHITE)
    d.text((107, 1152), note, font=f2, fill=accent)
    im.save(path)
    return path


def validate_source(source, output, expected_sha, genre, edit=EDIT):
    validate_config(genre)
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError('source overwrite forbidden')
    if not Path(source).is_file() or sha(source) != expected_sha:
        raise ValueError('source SHA mismatch')
    if len(edit) != 2 or not (14.25 <= edit[0] < edit[1] <= 17.35):
        raise ValueError('edit must stay in verified scene06')
    p = probe(source)
    v = next((s for s in p['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in p['streams'] if s['codec_type'] == 'audio'), None)
    if not v or (v['codec_name'], v['width'], v['height'], v['r_frame_rate']) != ('h264', 1080, 1920, '30/1'):
        raise ValueError('unsupported video format')
    if not a or (a['codec_name'], a['sample_rate']) != ('aac', '48000'):
        raise ValueError('unsupported audio format')
    if float(p['format']['duration']) < edit[1]:
        raise ValueError('video shorter than edit')
    return int(v['nb_frames'])


def render(source, output, expected_sha, genre='ai', edit=EDIT):
    frames = validate_source(source, output, expected_sha, genre, edit)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        png = make_overlay(Path(td) / 'provenance.png', genre)
        filt = f"[0:v][1:v]overlay=0:0:enable='gte(t,{edit[0]})*lt(t,{edit[1]})':eof_action=pass,format=yuv420p[v]"
        run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source), '-loop', '1', '-i', str(png),
             '-filter_complex', filt, '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-frames:v', str(frames), '-movflags', '+faststart', str(output)])
    q = probe(output)
    vv = next(s for s in q['streams'] if s['codec_type'] == 'video')
    if int(vv['nb_frames']) != frames:
        raise RuntimeError('frame count changed')
    return {'source_sha256': expected_sha, 'output_sha256': sha(output), 'frames': frames,
            'duration_seconds': float(q['format']['duration']), 'video': 'H264 1080x1920 30fps',
            'changed_seconds': list(edit), 'change': 'high-contrast fictional-data / human-review provenance',
            'audio_adts_identical': audio_sha(source) == audio_sha(output),
            'japanese_transcription': 'UNVERIFIED', 'caption_semantic_sync': 'UNVERIFIED',
            'rights': 'UNVERIFIED', 'publication': 'NOT_APPROVED'}


def main():
    p = argparse.ArgumentParser()
    for key in ('source', 'source-sha', 'out', 'report'):
        p.add_argument('--'+key, required=True)
    p.add_argument('--genre', choices=tuple(GENRE_ACCENTS), default='ai')
    a = p.parse_args()
    r = render(a.source, a.out, a.source_sha, a.genre)
    Path(a.report).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(r, ensure_ascii=False))

if __name__ == '__main__':
    main()
