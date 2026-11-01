"""Review-only numerical truth guard: no false intermediate totals on screen.

Overlays a tiny, source-calculated total card on scene06 of an existing
review MP4. Original audio and all Japanese subtitles are retained. This
is a reimplementation, not original v33 code. Never publish without approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
BOX = (728, 832, 294, 218)
SCENE = (429, 520)  # frames 429..519, 14.300..17.333 seconds
CAPTION_START_Y = 1490
PALETTES = {
    'ai_work': '#28d5c8', 'money': '#eebd68', 'career': '#7abfff',
    'business': '#7cdbad', 'health': '#ff9c9b', 'study': '#b5a5ff',
    'lifestyle': '#f6add8', 'technology': '#68d9ff', 'travel': '#ffd18b',
    'mindset': '#a5e6bc',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f'{cmd[0]} failed {p.returncode}: {p.stderr[-1500:]}')
    return p.stdout


def validate(m):
    required = {'genre', 'values', 'synthetic', 'review_only',
                'rights_status', 'contains_private_data', 'reveal_frame'}
    if set(m) != required or m.get('genre') not in PALETTES:
        raise ValueError('invalid manifest fields or genre')
    if (m['synthetic'] is not True or m['review_only'] is not True
            or m['rights_status'] != 'unverified'
            or m['contains_private_data'] is not False):
        raise ValueError('unapproved/non-synthetic/private input forbidden')
    if not isinstance(m['values'], dict) or set(m['values']) != {'営業A', '営業B'}:
        raise ValueError('source columns required')
    if any(type(v) is not int or v < 0 or v > 999 for v in m['values'].values()):
        raise ValueError('nonnegative integer source data required')
    if not 0 <= m['values']['営業A'] + m['values']['営業B'] <= 999:
        raise ValueError('sum out of display range')
    if type(m['reveal_frame']) is not int or not 0 <= m['reveal_frame'] < 91:
        raise ValueError('reveal frame out of range')
    return m['values']['営業A'] + m['values']['営業B']


def displayed_total(frame, m):
    total = validate(m)
    if type(frame) is not int or not 0 <= frame < 91:
        raise ValueError('frame outside proof scene')
    return None if frame < m['reveal_frame'] else total


def card(frame, m):
    shown = displayed_total(frame, m)
    accent = PALETTES[m['genre']]
    w, h = BOX[2:]
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, w-3, h-3), radius=17,
                        fill='#104b4b', outline=accent, width=3)
    d.text((20, 17), '合計', font=ImageFont.truetype(FONT, 27), fill='#e6f9fa')
    if shown is None:
        d.text((w//2, 117), '確認中', anchor='mm',
               font=ImageFont.truetype(FONT, 37), fill='#a7d2d5')
    else:
        d.text((w//2, 115), str(shown), anchor='mm',
               font=ImageFont.truetype(FONT, 73), fill=accent)
        if frame >= m['reveal_frame'] + 12:
            d.ellipse((w-41, 20, w-18, 43), fill=accent)
            d.line((w-36, 31, w-31, 36, w-23, 26), fill='#063b3c', width=3)
    return im


def render(source, out, expected_sha, m, start=SCENE[0], end=SCENE[1]):
    validate(m)
    if len(expected_sha) != 64 or sha256(source) != expected_sha:
        raise ValueError('source SHA256 mismatch: fail closed')
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                            '-show_format', '-of', 'json', str(source)]))
    videos = [s for s in probe['streams'] if s['codec_type'] == 'video']
    audios = [s for s in probe['streams'] if s['codec_type'] == 'audio']
    if (len(videos) != 1 or len(audios) != 1
            or (videos[0]['codec_name'], videos[0]['width'], videos[0]['height'],
                videos[0]['r_frame_rate']) != ('h264', 1080, 1920, '30/1')
            or (audios[0]['codec_name'], audios[0]['sample_rate']) != ('aac', '48000')):
        raise ValueError('expected 1080x1920/30 H264 + 48k AAC')
    if not (0 <= start < end <= int(float(probe['format']['duration']) * FPS + 1)):
        raise ValueError('invalid overlay window')
    if BOX[1] + BOX[3] >= CAPTION_START_Y:
        raise ValueError('subtitle collision')
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(end-start):
            card(i, m).save(f'{tmp}/ov_{i:03d}.png', compress_level=1)
        filtergraph = (f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start/FPS}/TB[ov];'
                       f"[0:v][ov]overlay={BOX[0]}:{BOX[1]}:eof_action=pass:repeatlast=0:"
                       f"enable='between(n,{start},{end-1})'[v]")
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
             '-framerate', str(FPS), '-i', f'{tmp}/ov_%03d.png',
             '-filter_complex', filtergraph, '-map', '[v]', '-map', '0:a:0',
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
             '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
             '-movflags', '+faststart', str(out)])
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'])
    return {'source_sha256': expected_sha, 'output_sha256': sha256(out),
            'changed_frames': [start, end-1], 'stable_total': validate(m),
            'reveal_frame': m['reveal_frame'], 'audio': 'AAC stream copy',
            'subtitle': 'overlay ends before y=1490',
            'publication': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def smoke():
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp)/'synthetic.mp4'
        out = Path(tmp)/'test.mp4'
        run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
             'color=c=0x123246:s=1080x1920:r=30:d=3', '-f','lavfi','-i',
             'sine=frequency=440:sample_rate=48000:duration=3',
             '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
             '-c:a','aac','-shortest',str(source)])
        m = json.loads((Path(__file__).parent/'manifest.json').read_text())
        m['reveal_frame'] = 10
        print(json.dumps(render(source,out,sha256(source),m,start=15,end=45),ensure_ascii=False))
        print('PASS: synthetic A/V full decode')


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source');p.add_argument('--source-sha')
    p.add_argument('--manifest');p.add_argument('--out');p.add_argument('--smoke',action='store_true')
    a=p.parse_args()
    if a.smoke: smoke()
    else:
        if not all([a.source,a.source_sha,a.manifest,a.out]):p.error('missing required render inputs')
        m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
        print(json.dumps(render(a.source,a.out,a.source_sha,m),ensure_ascii=False,indent=2))
