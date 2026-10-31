"""Review-only 10-genre habit storyboard. Never publishes or commits source media."""
import argparse
import hashlib
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, START, COUNT = 1080, 1450, 30, 609, 82
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
PALETTES = {
    'ai_work': '#21D7CB', 'finance': '#EDBE68', 'education': '#7FAEFF',
    'health': '#7DD6AC', 'travel': '#F4A9B8', 'beauty': '#D6A4F7',
    'food': '#FFAB75', 'career': '#6ED1E9', 'productivity': '#B8DF74',
    'lifestyle': '#F1C37B',
}
STEPS = (('今日', '1つだけ試す'), ('明日', '使える形で残す'), ('週末', '続けるか見直す'))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def stage(i):
    if not 0 <= i < COUNT:
        raise ValueError('frame outside scene')
    return min(2, i // 28)


def color(hexcode):
    return tuple(int(hexcode[j:j+2], 16) for j in (1, 3, 5))


def background(accent):
    y, x = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((x-860)/470)**2 + ((y-320)/440)**2))
    a = np.array(color(accent), dtype=np.float32)
    base = np.stack([7+6*y/H, 18+14*y/H, 32+16*y/H], axis=-1)
    rgb = np.clip(base + glow[..., None]*a*0.12, 0, 255).astype('uint8')
    return Image.fromarray(rgb, 'RGB')


def render_frame(i, genre='ai_work', base=None):
    if genre not in PALETTES:
        raise ValueError('unknown genre')
    p = stage(i)
    accent = PALETTES[genre]
    im = (base.copy() if base is not None else background(accent))
    d = ImageDraw.Draw(im)
    bold = lambda n: ImageFont.truetype(FONT, n)
    regular = lambda n: ImageFont.truetype(REG, n)
    d.rounded_rectangle((46, 50, 1034, 1222), radius=42, fill='#0B2537', outline='#436275', width=3)
    d.text((86, 102), 'SMALL STEPS  /  DAILY HABIT', font=bold(27), fill=accent)
    d.text((84, 170), '小さく始めて、続ける。', font=bold(58), fill='#F5FBFF')
    d.text((86, 260), '今日の1つを、明日の習慣に。', font=regular(33), fill='#C3D7E4')
    # Three independently reusable illustrated timeline cards.
    for j, (when, what) in enumerate(STEPS):
        top = 378 + 247*j
        active = j == p
        lift = int(8 * ease((i % 28) / 27)) if active else 0
        y0 = top-lift
        d.rounded_rectangle((92, y0+10, 993, y0+207), radius=28, fill='#061623')
        d.rounded_rectangle((88, y0, 989, y0+195), radius=28,
                            fill='#164253' if active else '#193243',
                            outline=accent if active else '#375568', width=4 if active else 2)
        d.rounded_rectangle((116, y0+37, 273, y0+150), radius=24,
                            fill=accent if active else '#2C5365')
        d.text((143, y0+67), when, font=bold(36), fill='#081F2D' if active else '#E1F1F8')
        d.text((318, y0+61), what, font=bold(42), fill='#FFFFFF' if active else '#B6CEDD')
        if j < p:
            d.ellipse((913, y0+72, 958, y0+117), fill=accent)
            d.text((923, y0+71), '✓', font=bold(29), fill='#082536')
        elif active:
            pulse = int(8 * math.sin(math.pi * ease((i % 28) / 27)))
            d.ellipse((915-pulse, y0+77-pulse, 948+pulse, y0+110+pulse),
                      outline=accent, width=4)
    d.text((92, 1151), '説明用の例示です / 効果時間の実測値ではありません', font=regular(25), fill='#B2CAD8')
    d.rounded_rectangle((46, 1262, 1034, 1425), radius=26, fill='#102D40', outline='#31576A', width=2)
    d.text((84, 1285), '1つ試して、明日も続けよう。', font=bold(37), fill='#E8F7FD')
    d.rounded_rectangle((84, 1370, 992, 1383), radius=6, fill='#355466')
    d.rounded_rectangle((84, 1370, 84 + int(908 * (i + 1) / COUNT), 1383), radius=6, fill=accent)
    return im


def parse_srt(text):
    pattern = re.compile(r'(\d+)\s*\n(\d\d:\d\d:\d\d,\d{3})\s*-->\s*(\d\d:\d\d:\d\d,\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)', re.S)
    def seconds(s):
        hh, mm, rest = s.split(':'); ss, ms = rest.split(',')
        return int(hh)*3600+int(mm)*60+int(ss)+int(ms)/1000
    return [(int(n), seconds(a), seconds(b), ' '.join(t.strip().splitlines()))
            for n, a, b, t in pattern.findall(text)]


def audio_audit(video, srt):
    items = parse_srt(Path(srt).read_text(encoding='utf-8'))
    if len(items) != 8 or any(not txt or end <= start for _,start,end,txt in items):
        raise ValueError('expected eight nonempty timed Japanese captions')
    pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(video), '-vn',
                                   '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
    audio = np.frombuffer(pcm, dtype='<f4')
    results = []
    for n, a, b, txt in items:
        chunk = audio[round(a*16000):round(b*16000)]
        rms = float(np.sqrt(np.mean(chunk.astype('float64')**2))) if len(chunk) else 0
        results.append({'section': n, 'start': a, 'end': b, 'rms_dbfs': round(20*math.log10(max(rms, 1e-9)), 2),
                        'text': txt, 'signal_present': rms > 0.001})
    return {'sections': results, 'all_sections_have_audio_energy': all(z['signal_present'] for z in results),
            'semantic_transcription': 'NOT_TESTED', 'word_alignment': 'NOT_TESTED',
            'boundary_20_300_s': 'ENERGY_ONLY_NOT_SEMANTIC'}


def compose(source, out, work, expected_sha, genre='ai_work'):
    if genre not in PALETTES or sha256(source) != expected_sha:
        raise ValueError('invalid genre or private input SHA mismatch')
    frames = Path(work) / 'frames'; frames.mkdir(parents=True, exist_ok=True)
    bg = background(PALETTES[genre])
    for i in range(COUNT):
        render_frame(i, genre, bg).save(frames / f'f_{i:03d}.png')
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-framerate', str(FPS), '-start_number', '0', '-i', str(frames / 'f_%03d.png'),
        '-filter_complex', f'[1:v]setpts=PTS+{START/FPS:.9f}/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
        '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
        '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
        '-movflags', '+faststart', str(out)], check=True)


def smoke():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td); bg = background(PALETTES['ai_work'])
        for i in range(15): render_frame(i, base=bg).save(p/f'f_{i:03d}.png')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '30',
            '-i', str(p/'f_%03d.png'), '-f', 'lavfi', '-i',
            'sine=frequency=440:sample_rate=48000:duration=0.5', '-c:v', 'libx264',
            '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(p/'smoke.mp4')], check=True)
        streams = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p/'smoke.mp4')]))['streams']
        assert {s['codec_name'] for s in streams} == {'h264','aac'}
        subprocess.run(['ffmpeg','-v','error','-i',str(p/'smoke.mp4'),'-f','null','-'], check=True)
        print('PASS synthetic H264/AAC smoke; private full MP4 excluded from CI')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    for name in ('source','out','work','source-sha256','srt','audit-out'): ap.add_argument('--'+name)
    ap.add_argument('--genre',default='ai_work'); ap.add_argument('--smoke',action='store_true')
    a = ap.parse_args()
    if a.smoke: smoke()
    else:
        compose(a.source,a.out,a.work,a.source_sha256,a.genre)
        if a.srt:
            audit=audio_audit(a.out,a.srt)
            Path(a.audit_out).write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
