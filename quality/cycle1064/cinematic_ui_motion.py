"""Original, caption-safe Ken Burns motion over a sanitized real-app screenshot.

No live operation is claimed: GUI image is static; motion and overlays are authored.
The private screenshot and source video are never committed to GitHub.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1270, 30
START, COUNT = 174, 82
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PALETTES = {
    'ai_work': '#21D7CB', 'finance': '#EDBE68', 'education': '#7FAEFF',
    'health': '#7DD6AC', 'travel': '#F4A9B8', 'beauty': '#D6A4F7',
    'food': '#FFAB75', 'career': '#6ED1E9', 'productivity': '#B8DF74',
    'lifestyle': '#F1C37B',
}
LABELS = ('実アプリの見本', '数字を照合', '見本として残す')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def phase(i):
    if not 0 <= i < COUNT:
        raise ValueError('invalid frame')
    return min(2, i // 28)


def motion(i):
    if not 0 <= i < COUNT:
        raise ValueError('invalid frame')
    t = smoothstep(i / (COUNT - 1))
    return (1.0 + 0.085 * t, round(-28 * t), round(-15 * t))


def render_frame(i, screenshot, genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unknown genre')
    shot = screenshot if isinstance(screenshot, Image.Image) else Image.open(screenshot)
    if shot.size != (1600, 900):
        raise ValueError('sanitized screenshot must be 1600x900')
    shot = shot.convert('RGB')
    accent = PALETTES[genre]
    font = lambda n: ImageFont.truetype(FONT, n)
    # Soft cinematic gradient is original artwork; no stock assets.
    im = Image.new('RGB', (W, H))
    pix = im.load()
    for y in range(H):
        r = int(7 + 6 * y / H)
        g = int(19 + 15 * y / H)
        b = int(34 + 18 * y / H)
        for x in range(W):
            pix[x, y] = (r, g, b)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((42, 36, 1038, 1220), radius=42, fill='#0A2435', outline='#37576A', width=3)
    d.text((84, 92), '完成形を、画面で確認。', font=font(49), fill='#F5FAFD')
    d.text((86, 173), 'REAL APP SCREENSHOT  /  FICTIONAL DATA', font=font(23), fill='#A3C0D2')
    # Glass card shadow and the unmodified Calc screenshot in a moving crop.
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((62, 320, 1022, 942), radius=35, fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im.convert('RGBA'), shadow.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((62, 303, 1018, 922), radius=30, fill='#EAF1F5', outline='#608497', width=3)
    crop = shot.crop((57, 275, 580, 480))
    scale, dx, dy = motion(i)
    tw, th = int(908 * scale), int(480 * scale)
    crop = crop.resize((tw, th), Image.Resampling.LANCZOS)
    # The viewport stays inside the panel, with a slight 2.7s push-in.
    viewport = Image.new('RGB', (908, 480), '#F2F5F6')
    viewport.paste(crop, ((908 - tw) // 2 + dx, (480 - th) // 2 + dy))
    im.paste(viewport, (86, 358))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((82, 975, 998, 1070), radius=19, fill='#123C4D')
    p = phase(i)
    for j, label in enumerate(LABELS):
        x = 88 + j * 305
        d.rounded_rectangle((x, 1000, x + 286, 1047), radius=13,
                            fill='#1D6973' if j == p else '#23485A',
                            outline=accent if j == p else '#3D6374', width=2)
        d.text((x + 12, 1007), label, font=font(23), fill='#FFFFFF')
    d.text((87, 1112), '実アプリ画面の静止画にズーム演出を追加 / 操作録画ではありません',
           font=font(23), fill='#B6D0DC')
    d.rounded_rectangle((87, 1170, 992, 1180), radius=5, fill='#345B6A')
    d.rounded_rectangle((87, 1170, 87 + int(905 * (i + 1) / COUNT), 1180), radius=5, fill=accent)
    return im.convert('RGB')


def compose(source, screenshot, output, work, source_sha256, screenshot_sha256, genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unknown genre')
    for path, digest in ((source, source_sha256), (screenshot, screenshot_sha256)):
        if not digest or len(digest) != 64 or sha256(path) != digest:
            raise ValueError('private input SHA mismatch')
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = Path(work) / 'frames'
    frames.mkdir(parents=True, exist_ok=True)
    shot = Image.open(screenshot).convert('RGB')
    for i in range(COUNT):
        render_frame(i, shot, genre).save(frames / f'frame_{i:03d}.png')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-framerate', str(FPS), '-start_number', '0', '-i', str(frames / 'frame_%03d.png'),
        '-filter_complex', f'[1:v]setpts=PTS+{START/FPS:.9f}/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
        '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
        '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
        '-movflags', '+faststart', str(out)], check=True)


def smoke():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        shot = Image.new('RGB', (1600, 900), 'white')
        for i in range(15):
            render_frame(i, shot).save(p / f'f_{i:03d}.png')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '30',
            '-i', str(p / 'f_%03d.png'), '-f', 'lavfi', '-i',
            'sine=frequency=440:sample_rate=48000:duration=0.5',
            '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', str(p / 'smoke.mp4')], check=True)
        streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
            '-show_streams', '-of', 'json', str(p / 'smoke.mp4')]))['streams']
        assert {s['codec_name'] for s in streams} == {'h264', 'aac'}
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p / 'smoke.mp4'), '-f', 'null', '-'], check=True)
        print('PASS synthetic smoke H264/AAC; private 23s MP4 excluded from CI')


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    for field in ('source', 'screenshot', 'out', 'work', 'source-sha256', 'screenshot-sha256'):
        a.add_argument('--' + field)
    a.add_argument('--genre', default='ai_work')
    a.add_argument('--smoke', action='store_true')
    opts = a.parse_args()
    if opts.smoke:
        smoke()
    else:
        compose(opts.source, opts.screenshot, opts.out, opts.work,
                opts.source_sha256, opts.screenshot_sha256, opts.genre)
