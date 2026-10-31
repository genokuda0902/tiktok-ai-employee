"""cycle1070: review-only, rights-preserving output-format field reveal.

10-genre reusable overlay. Works on an approved local source only after SHA256
allowlist verification. Never uploads private media; no posting or automatic merge.
This is a reimplementation, not the recovered original v33 source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SCENE_START_FRAME, SCENE_END_FRAME = 256, 342  # [256,342), scene 04
REVEAL_FIRST_LOCAL_FRAME = 57
REVEAL_FRAMES = 15
PANEL_TOP, PANEL_H = 840, 170
MASK = (173, 60, 722, 119)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FORMATS = {
    'ai_work': '月別比較表（CSV形式）',
    'finance': '費目別の集計表（CSV）',
    'education': '単元別の復習表（CSV）',
    'health': '生活記録の一覧表（CSV）',
    'travel': '日別の行程表（CSV）',
    'beauty': '項目別の比較表（CSV）',
    'food': '材料別の買い物表（CSV）',
    'career': '応募先の比較表（CSV）',
    'productivity': '作業別の時短表（CSV）',
    'lifestyle': '習慣別の記録表（CSV）',
}
PALETTES = {
    'ai_work': '#21D7CB', 'finance': '#EDBE68', 'education': '#7FAEFF',
    'health': '#7DD6AC', 'travel': '#F4A9B8', 'beauty': '#D6A4F7',
    'food': '#FFAB75', 'career': '#6ED1E9', 'productivity': '#B8DF74',
    'lifestyle': '#F1C37B',
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def spec(path):
    d = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    a = next(s for s in d['streams'] if s['codec_type'] == 'audio')
    return {'width': v['width'], 'height': v['height'], 'fps': v['r_frame_rate'],
            'video': v['codec_name'], 'audio': a['codec_name'],
            'duration': float(d['format']['duration'])}

def visible_chars(local_frame, text):
    if local_frame < REVEAL_FIRST_LOCAL_FRAME:
        return 0
    # Half-second typing, then hold the complete example for legibility.
    return min(len(text), (local_frame - REVEAL_FIRST_LOCAL_FRAME) * len(text) // REVEAL_FRAMES)

def overlay_frame(local_frame, genre='ai_work'):
    if genre not in FORMATS:
        raise ValueError('unsupported genre')
    if not 0 <= local_frame < SCENE_END_FRAME - SCENE_START_FRAME:
        raise ValueError('frame out of range')
    im = Image.new('RGBA', (W, PANEL_H), (0, 0, 0, 0))
    if local_frame < REVEAL_FIRST_LOCAL_FRAME:
        return im
    d = ImageDraw.Draw(im)
    # Only fill the placeholder bar, not the card title, subtitles or scene bridge.
    d.rectangle(MASK, fill=(11, 44, 65, 255))
    font = ImageFont.truetype(FONT, 30)
    text = FORMATS[genre]
    count = visible_chars(local_frame, text)
    shown = text[:count]
    d.text((176, 64), shown, font=font, fill=(244, 251, 255, 255))
    # Animated caret clarifies that this is an example output-format field.
    extent = d.textbbox((176, 64), shown, font=font)
    x = min(extent[2] + 8, 711)
    d.rounded_rectangle((x, 70, x + 4, 100), radius=2, fill=PALETTES[genre])
    return im

def check_layout():
    font = ImageFont.truetype(FONT, 30)
    im = Image.new('RGB', (W, PANEL_H))
    d = ImageDraw.Draw(im)
    for genre, txt in FORMATS.items():
        if d.textbbox((176, 64), txt, font=font)[2] > 702:
            raise ValueError('format example too long: ' + genre)
    return True

def compose(source, out, expected_sha, genre='ai_work'):
    if genre not in FORMATS:
        raise ValueError('unsupported genre')
    check_layout()
    if sha256(source) != expected_sha:
        raise ValueError('source SHA256 mismatch (fail closed)')
    inp = spec(source)
    if (inp['width'], inp['height'], inp['fps'], inp['video'], inp['audio']) != (W, H, '30/1', 'h264', 'aac'):
        raise ValueError('unexpected input streams')
    if abs(inp['duration'] - 23.033333) > 0.1:
        raise ValueError('unexpected source duration')
    with tempfile.TemporaryDirectory() as td:
        folder = Path(td)
        for i in range(SCENE_END_FRAME - SCENE_START_FRAME):
            overlay_frame(i, genre).save(folder / f'{i:04d}.png')
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-i', str(source), '-framerate', str(FPS), '-start_number', '0',
               '-i', str(folder / '%04d.png'), '-filter_complex',
               '[1:v]format=rgba,setpts=PTS+256/30/TB[ol];'
               '[0:v][ol]overlay=x=0:y=840:eof_action=pass:shortest=0:format=auto[v]',
               '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264',
               '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
               '-r', str(FPS), '-frames:v', '691', '-c:a', 'copy',
               '-movflags', '+faststart', str(out)]
        subprocess.run(cmd, check=True)
    return spec(out)

def smoke():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        src, dst = root/'synthetic.mp4', root/'synthetic_out.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        'color=c=#0b2c41:s=1080x1920:r=30:d=23.033333',
                        '-f', 'lavfi', '-i',
                        'sine=frequency=440:sample_rate=48000:duration=23.033333',
                        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-shortest', str(src)], check=True)
        s = compose(src, dst, sha256(src))
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(dst), '-f', 'null', '-'], check=True)
        assert s['video'] == 'h264' and s['audio'] == 'aac'
        print('PASS synthetic 23s full H264/AAC decode; no private media')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source')
    ap.add_argument('--out')
    ap.add_argument('--source-sha256')
    ap.add_argument('--genre', default='ai_work')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    if a.smoke:
        smoke()
    else:
        print(json.dumps(compose(a.source, a.out, a.source_sha256, a.genre), indent=2))
