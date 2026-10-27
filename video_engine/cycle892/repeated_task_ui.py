"""cycle892: original, synthetic spreadsheet-like workflow illustration.

NOT Excel or a commercial-service recording. Fictional values only.
Source MP4 stays local; release approval is fail-closed.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
START, END = 89, 170
FRAMES = 691
PATCH_X, PATCH_Y, PATCH_W, PATCH_H = 70, 650, 940, 530
GENRES = ('ai_productivity', 'beauty', 'romance_psychology', 'money_saving',
          'sales_business', 'career', 'health_lifestyle', 'trivia_science',
          'travel_food', 'product_lifestyle')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
REVIEW_POLICY = {
    'review_only': True,
    'publication_approved': False,
    'external_upload': False,
    'automatic_posting': False,
    'source_rights_reviewed': False,
    'synthetic_ui': True,
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def font(size):
    if not Path(FONT).exists():
        raise RuntimeError('Japanese Noto font required')
    return ImageFont.truetype(FONT, size)

def validate_rows(rows):
    if not isinstance(rows, list) or len(rows) != 3:
        raise ValueError('Exactly 3 synthetic rows required')
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'label', 'a', 'b'}:
            raise ValueError('Bad row schema')
        label = row['label']
        if not isinstance(label, str) or not 1 <= len(label) <= 7 or re.search(r'[@<>\n\r]|https?://|\d{8}', label):
            raise ValueError('Unsafe label')
        for k in ('a', 'b'):
            if type(row[k]) is not int or not 0 <= row[k] <= 999:
                raise ValueError('Unsafe value')
    return True

def validate_manifest(m, source):
    if not isinstance(m, dict):
        raise ValueError('Manifest must be object')
    if any(m.get(k) != v for k, v in REVIEW_POLICY.items()):
        raise ValueError('Fail-closed review policy')
    if m.get('genre') not in GENRES:
        raise ValueError('Unsupported genre')
    if m.get('source_sha256') != sha256(source):
        raise ValueError('Unpinned source')
    validate_rows(m.get('rows'))
    return True

def stage_at(local_frame):
    if type(local_frame) is not int or not 0 <= local_frame < END - START:
        raise ValueError('Out-of-range frame')
    return min(2, local_frame // 27)

def eased(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3

def draw_patch(local_frame, rows):
    validate_rows(rows)
    stage = stage_at(local_frame)
    phase = (local_frame % 27) / 26
    fade = eased(min(1.0, phase * 3.3))
    im = Image.new('RGBA', (PATCH_W, PATCH_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 939, 529), radius=27, fill=(5, 23, 42, 252), outline=(61, 176, 206, 255), width=4)
    d.rounded_rectangle((18, 15, 922, 72), radius=14, fill=(14, 52, 74, 255))
    d.text((38, 20), '繰り返し作業を発見する', font=font(31), fill='white')
    d.text((694, 27), '再現UI / 架空データ', font=font(17), fill=(173, 221, 231))
    left, top = 35, 90
    widths = [175, 220, 220, 235]
    xs = [left]
    for w in widths: xs.append(xs[-1] + w)
    headers = ('月', '営業A', '営業B', '作業')
    d.rounded_rectangle((left, top, xs[-1], top + 67), radius=9, fill=(22, 79, 108))
    for c, name in enumerate(headers):
        d.text((xs[c] + 22, top + 14), name, font=font(28), fill=(230, 250, 255))
    for i, row in enumerate(rows):
        y0 = top + 67 + i * 78
        active = i == stage
        base = (23, 87, 112, 255) if active else ((11, 40, 62, 255) if i % 2 == 0 else (12, 47, 67, 255))
        d.rectangle((left, y0, xs[-1], y0 + 76), fill=base)
        for c, value in enumerate((row['label'], str(row['a']), str(row['b']), '手動集計')):
            d.text((xs[c] + 22, y0 + 16), value, font=font(29 if c < 3 else 26), fill=(246, 251, 255))
        if active:
            alpha = int(255 * fade)
            d.rounded_rectangle((left + 3, y0 + 3, xs[-1] - 3, y0 + 74), radius=10,
                                outline=(72, 233, 237, alpha), width=6)
            x = xs[-2] + 175 + int(12 * (1 - fade))
            y = y0 + 30
            d.polygon([(x, y), (x + 21, y + 35), (x + 26, y + 21), (x + 40, y + 19)],
                      fill=(255, 230, 125, alpha))
    for x in xs[1:-1]: d.line((x, top, x, top + 301), fill=(60, 115, 135), width=2)
    d.rounded_rectangle((35, 410, 905, 503), radius=15, fill=(9, 65, 88, 255))
    tasks = ('毎月同じデータを転記', '毎月同じ計算を実施', '毎月同じ数字を確認')
    d.text((58, 426), f'{stage + 1} / 3', font=font(34), fill=(105, 240, 245))
    d.text((205, 429), tasks[stage], font=font(31), fill='white')
    for i in range(3):
        x = 205 + i * 210
        d.rounded_rectangle((x, 479, x + 190, 487), radius=4,
                            fill=(48, 210, 224) if i <= stage else (54, 97, 113))
    return im

def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of', 'json', str(path)], text=True))

def render(source, output, manifest, work, report):
    source, output, work, report = map(Path, (source, output, work, report))
    m = json.loads(Path(manifest).read_text(encoding='utf-8'))
    validate_manifest(m, source)
    spec = probe(source)
    v = next(s for s in spec['streams'] if s['codec_type'] == 'video')
    a = next(s for s in spec['streams'] if s['codec_type'] == 'audio')
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate'], int(v['nb_frames'])) != ('h264', 1080, 1920, '30/1', FRAMES):
        raise ValueError('Unexpected video specification')
    if (a['codec_name'], int(a['sample_rate']), a['channels']) != ('aac', 48000, 2):
        raise ValueError('Unexpected audio specification')
    if PATCH_X < 60 or PATCH_X + PATCH_W > 1020 or PATCH_Y + PATCH_H > 1280:
        raise ValueError('Subtitle overlap risk')
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    for i in range(END - START):
        draw_patch(i, m['rows']).save(work / f'{i:03d}.png', compress_level=2)
    filt = (f'[1:v]format=rgba,setpts=PTS+{START}/({FPS}*TB)[ov];'
            f"[0:v][ov]overlay={PATCH_X}:{PATCH_Y}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]")
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-framerate', str(FPS), '-start_number', '0', '-i', str(work / '%03d.png'),
        '-filter_complex', filt, '-map', '[v]', '-map', '0:a:0', '-frames:v', str(FRAMES),
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
        '-c:a', 'copy', '-movflags', '+faststart', str(output)], check=True, timeout=300)
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output), '-f', 'null', '-'],
                   check=True, timeout=120)
    result = {'cycle': 892, 'source_sha256': sha256(source), 'output_sha256': sha256(output),
              'scene_frames': END - START, 'full_av_decode': 'PASS',
              'original_ui': 'synthetic_offline_not_excel', 'japanese_asr': 'UNVERIFIED',
              'semantic_caption_match': 'UNVERIFIED', 'publication': 'NOT_APPROVED'}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for n in ('source', 'output', 'manifest', 'work', 'report'):
        p.add_argument('--' + n, required=True)
    args = p.parse_args()
    print(json.dumps(render(args.source, args.output, args.manifest, args.work, args.report), ensure_ascii=False))
