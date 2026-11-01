"""Review-only, evidence-linked final-scene CTA. Not the original v33 engine.

The source clip and any extracted frames stay local; never commit source media.
A SHA pin is integrity checking, NOT publication-rights clearance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
START, END, PROTECTED_Y = 609, 691, 1490
PALETTES = {
    'ai_work': '#24ddcf', 'money': '#eebd68', 'career': '#7abfff',
    'business': '#7cdbad', 'health': '#ff9c9b', 'study': '#b5a5ff',
    'lifestyle': '#f6add8', 'technology': '#68d9ff', 'travel': '#ffd18b',
    'mindset': '#a5e6bc',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as file:
        for part in iter(lambda: file.read(1 << 20), b''):
            h.update(part)
    return h.hexdigest()


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'{args[0]} exit={r.returncode}: {r.stderr[-1600:]}')
    return r.stdout


def check_manifest(data):
    required = {'genre', 'topic', 'headline', 'detail', 'steps', 'preview_time',
                'preview_crop', 'synthetic', 'review_only', 'rights_status', 'contains_private_data'}
    if set(data) != required:
        raise ValueError('missing/extra manifest fields')
    if data['genre'] not in PALETTES:
        raise ValueError('unsupported genre')
    if data['synthetic'] is not True or data['review_only'] is not True:
        raise ValueError('only synthetic private review permitted')
    if data['rights_status'] != 'unverified' or data['contains_private_data'] is not False:
        raise ValueError('fail closed: review rights/privacy metadata')
    if not isinstance(data['steps'], list) or len(data['steps']) != 3:
        raise ValueError('exactly three steps required')
    for field, max_len in [('topic', 24), ('headline', 26), ('detail', 38)]:
        if not isinstance(data[field], str) or not 1 <= len(data[field]) <= max_len:
            raise ValueError(f'invalid {field}')
    if any(not isinstance(s, str) or not 1 <= len(s) <= 12 for s in data['steps']):
        raise ValueError('invalid step')
    if not isinstance(data['preview_time'], (int, float)) or not 0 <= data['preview_time'] < START / FPS:
        raise ValueError('preview must precede CTA')
    crop = data['preview_crop']
    if not isinstance(crop, list) or len(crop) != 4 or any(type(x) is not int for x in crop):
        raise ValueError('invalid crop')
    x0, y0, x1, y1 = crop
    if not (0 <= x0 < x1 <= WIDTH and 0 <= y0 < y1 <= PROTECTED_Y):
        raise ValueError('crop outside non-caption region')
    return True


def check_source(path, expected):
    if not expected or len(expected) != 64 or sha256(path) != expected:
        raise ValueError('source SHA256 mismatch or missing; fail closed')


def probe(path):
    raw = run(['ffprobe', '-v', 'error', '-show_entries',
               'stream=codec_name,width,height,r_frame_rate,sample_rate',
               '-show_entries', 'format=duration', '-of', 'json', str(path)])
    obj = json.loads(raw)
    video = [s for s in obj['streams'] if s.get('codec_name') == 'h264']
    audio = [s for s in obj['streams'] if s.get('codec_name') == 'aac']
    if len(video) != 1 or len(audio) != 1:
        raise ValueError('expected exactly one H264 video and AAC audio')
    if (video[0].get('width'), video[0].get('height'), video[0].get('r_frame_rate'),
        int(audio[0].get('sample_rate', 0))) != (WIDTH, HEIGHT, '30/1', 48000):
        raise ValueError('unexpected video/audio specification')
    duration = float(obj['format']['duration'])
    if not 23.0 <= duration <= 23.1:
        raise ValueError('unexpected source duration')
    return duration


def extract_preview(path, seconds, crop, output):
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{seconds:.3f}', '-i', str(path),
         '-frames:v', '1', str(output)])
    image = Image.open(output).convert('RGB')
    return image.crop(tuple(crop))


def font(size):
    return ImageFont.truetype(FONT, size)


def color_rgb(code):
    return tuple(bytes.fromhex(code.lstrip('#')))


def render_frame(i, manifest, preview):
    check_manifest(manifest)
    if not 0 <= i < END - START:
        raise ValueError('frame index outside final scene')
    accent = PALETTES[manifest['genre']]
    ar, ag, ab = color_rgb(accent)
    # Opaque replacement of the off-topic habit tracker; existing audio/subtitles untouched.
    image = Image.new('RGBA', (WIDTH, PROTECTED_Y), '#06192a')
    d = ImageDraw.Draw(image)
    for y in range(0, PROTECTED_Y, 6):
        glow = int(11 * (1 - y / PROTECTED_Y))
        d.rectangle((0, y, WIDTH, y + 6), fill=(6, 25 + glow, 42 + glow, 255))
    for x in range(0, WIDTH, 90):
        d.line((x, 0, x, PROTECTED_Y), fill=(23, 54, 70, 255), width=1)
    d.rounded_rectangle((54, 48, 1026, 1214), radius=30,
                        fill='#092538', outline='#416878', width=3)
    d.rounded_rectangle((88, 84, 384, 139), radius=17,
                        fill='#103b4b', outline=accent, width=2)
    d.text((108, 91), manifest['topic'], font=font(27), fill='#e5f9ff')
    d.text((92, 173), manifest['headline'], font=font(53), fill='#f4faff')
    d.text((95, 253), manifest['detail'], font=font(29), fill='#a7ceda')
    # Evidence-linked preview, extracted from the earlier *same* video.
    d.rounded_rectangle((84, 341, 996, 868), radius=24,
                        fill='#12374b', outline=accent, width=3)
    preview = preview.resize((884, 488), Image.Resampling.LANCZOS)
    mask = Image.new('L', preview.size)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 883, 487), radius=17, fill=255)
    image.paste(preview, (98, 359), mask)
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((111, 372, 448, 415), radius=12, fill='#092538')
    d.text((126, 375), '架空データ / 実画面の例', font=font(23), fill='#ffffff')
    d.text((94, 906), '確認した内容を、次の作業へ。', font=font(34), fill='#eff9fc')
    for j, label in enumerate(manifest['steps']):
        x = 91 + j * 304
        active = i >= (8 + j * 20)
        d.rounded_rectangle((x, 974, x + 285, 1077), radius=16,
                            fill=('#135061' if active else '#123144'),
                            outline=(accent if active else '#406374'), width=3)
        d.text((x + 15, 997), f'{j + 1:02d}', font=font(28), fill=accent)
        d.text((x + 72, 994), label, font=font(26), fill='#ffffff' if active else '#a9c0cc')
        if active:
            d.ellipse((x + 250, 989, x + 273, 1012), fill=accent)
    d.rounded_rectangle((93, 1120, 986, 1131), radius=5, fill='#24485b')
    width = int(893 * min(1.0, (i + 1) / (END - START)))
    d.rounded_rectangle((93, 1120, 93 + max(10, width), 1131), radius=5, fill=accent)
    d.text((94, 1152), '説明用の架空例 / 公開・投稿は未承認', font=font(21), fill='#9fbac7')
    # Replace the former habit-tracker footer too; the real Japanese subtitle starts at y~1500.
    d.rounded_rectangle((54, 1248, 1026, 1445), radius=26, fill='#092538', outline='#416878', width=3)
    d.text((98, 1280), '46  +  29  =  75', font=font(64), fill='#ffffff')
    d.text((102, 1381), '架空の集計例を確認して、次の作業へ。', font=font(28), fill='#a7ceda')
    # This returned image has no pixels at y>=1490; original Japanese captions remain untouched.
    return image


def render(source, out, expected_sha, manifest):
    check_manifest(manifest)
    check_source(source, expected_sha)
    duration = probe(source)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        preview = extract_preview(source, manifest['preview_time'], manifest['preview_crop'], tmp / 'preview.png')
        for i in range(END - START):
            render_frame(i, manifest, preview).save(tmp / f'ov_{i:03d}.png', compress_level=1)
        flt = (f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START / FPS}/TB[ov];'
               f"[0:v][ov]overlay=0:0:eof_action=pass:repeatlast=0:enable='between(n,{START},{END - 1})'[v]")
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-framerate', str(FPS),
             '-i', str(tmp / 'ov_%03d.png'), '-filter_complex', flt,
             '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
             '-movflags', '+faststart', str(out)])
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'])
    return {'input_sha256': expected_sha, 'output_sha256': sha256(out),
            'changed_frames': [START, END - 1], 'duration': duration,
            'genre': manifest['genre'], 'audio': 'AAC stream copy',
            'protected': 'Overlay limited to y<1490; original subtitle at y>=1490 retained',
            'publication': 'NOT APPROVED'}


def smoke():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        src = p / 'synthetic.mp4'
        out = p / 'review.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
             'color=c=0x123246:s=1080x1920:r=30:d=23.033333', '-f', 'lavfi',
             '-i', 'sine=frequency=440:sample_rate=48000:duration=23.033333',
             '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-shortest', str(src)])
        manifest = json.loads((Path(__file__).parent / 'synthetic_manifest.json').read_text())
        print(json.dumps(render(src, out, sha256(src), manifest), ensure_ascii=False))
        print('PASS: synthetic H264/AAC 1080x1920 30fps full decode')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source')
    parser.add_argument('--source-sha')
    parser.add_argument('--manifest')
    parser.add_argument('--out')
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.smoke:
        smoke()
    else:
        if not all([args.source, args.source_sha, args.manifest, args.out]):
            parser.error('source, SHA, manifest and output required')
        m = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
        print(json.dumps(render(args.source, args.out, args.source_sha, m), ensure_ascii=False, indent=2))
