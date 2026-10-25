"""cycle851: factual local Calc correction inset for a 10-genre review-only TikTok video.

The screenshot is an actual isolated LibreOffice Calc GUI capture containing
invented sales figures. It is not a recording of ChatGPT or of a real business.
This is a reimplementation, NOT the original v33 generator. Rights are not
cleared for publication. Original Japanese audio/captions remain unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES = (
    'ai_work', 'sales_business', 'beauty', 'romance', 'saving',
    'career', 'wellness', 'science', 'travel_food', 'product_comparison_lifestyle'
)
POLICY = {
    'review_only': True,
    'publication_approved': False,
    'automatic_posting': False,
    'external_upload': False,
    'source_rights_reviewed': False,
    'contains_personal_data': False,
    'capture_is_fictional': True,
    'capture_is_real_local_gui': True,
}
PANEL = (86, 476, 994, 1234)
WINDOW = (422, 507)
PALETTES = {g: (28 + (i * 11) % 38, 201 - (i * 7) % 35, 198 - (i * 5) % 32)
            for i, g in enumerate(GENRES)}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format',
        '-of', 'json', str(path)], text=True))


def streams(path):
    s = probe(path)['streams']
    return (next((x for x in s if x['codec_type'] == 'video'), None),
            next((x for x in s if x['codec_type'] == 'audio'), None))


def validate(source, capture, output, manifest, genre, window):
    source, capture, output = map(Path, (source, capture, output))
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('unknown genre')
    if not source.is_file() or not capture.is_file():
        raise FileNotFoundError('local source or capture missing')
    expected = {**POLICY, 'source_sha256': sha256(source),
                'capture_sha256': sha256(capture)}
    if manifest != expected:
        raise ValueError('fail-closed provenance manifest mismatch')
    if output.exists() or output.resolve() in (source.resolve(), capture.resolve()):
        raise ValueError('overwrite forbidden')
    if len(window) != 2 or any(type(x) is not int for x in window):
        raise ValueError('invalid frame window')
    v, a = streams(source)
    if not v or not a or (v['codec_name'], v['width'], v['height'],
                          v['r_frame_rate'], a['codec_name']) != (
                              'h264', 1080, 1920, '30/1', 'aac'):
        raise ValueError('source must be H264 1080x1920 30fps + AAC')
    cv, _ = streams(capture)
    if not cv or cv['width'] < 1130 or cv['height'] < 385 or cv['r_frame_rate'] != '30/1':
        raise ValueError('capture must be 30fps genuine 1440x900-style GUI')
    n = int(v['nb_frames'])
    if not 0 <= window[0] < window[1] <= n:
        raise ValueError('window out of range')
    if window[1] - window[0] > int(cv['nb_frames']):
        raise ValueError('capture shorter than replacement window')
    return n


def stage(local_frame, total):
    if not 0 <= local_frame < total:
        raise ValueError('frame outside edit window')
    # Aligned to recorded action: edit begins at capture frame ~35; formula
    # recalculates at ~45; verification cursor is on D6 after frame ~75.
    if local_frame < round(total * 0.35):
        return 0
    if local_frame < round(total * 0.67):
        return 1
    return 2


def font(size):
    return ImageFont.truetype(FONT, size)


def panel_image(capture_bgr, local_frame, total, genre):
    if capture_bgr.shape[0] < 385 or capture_bgr.shape[1] < 1130:
        raise ValueError('capture image too small')
    st = stage(local_frame, total)
    accent = PALETTES[genre]
    bg = Image.new('RGB', (908, 758), (3, 18, 32))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((8, 8, 900, 750), radius=22,
                        outline=accent, width=4, fill=(6, 29, 45))
    d.rounded_rectangle((24, 24, 882, 121), radius=15, fill=(10, 51, 68))
    d.text((48, 52), '実際のCalc操作', font=font(41), fill=(255, 255, 255))
    d.text((847, 70), '架空データ', font=font(26), anchor='rm',
           fill=(173, 233, 235))

    # Real screenshot: preserve aspect ratio and avoid fabricating GUI contents.
    crop = capture_bgr[145:380, 245:1130]
    if crop.size == 0:
        raise ValueError('empty GUI crop')
    ui = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    ui = ui.resize((854, 227), Image.Resampling.LANCZOS)
    bg.paste(ui, (27, 145))
    d.rectangle((26, 144, 882, 374), outline=(105, 220, 227), width=3)
    d.text((40, 393), '数値と判定が連動して更新される', font=font(30),
           fill=(209, 229, 236))

    labels = [
        ('不一致を発見', '17  ≠  18', (255, 124, 126)),
        ('値を修正', '17  →  18', (255, 207, 112)),
        ('再計算で一致', '18  =  18', (71, 229, 177)),
    ]
    heading, equation, tone = labels[st]
    d.rounded_rectangle((35, 445, 873, 661), radius=20,
                        fill=(9, 39, 56), outline=tone, width=4)
    d.text((454, 485), heading, anchor='mm', font=font(43), fill=tone)
    d.text((454, 590), equation, anchor='mm', font=font(78),
           fill=(255, 255, 255))
    for i in range(3):
        d.rounded_rectangle((338 + i * 81, 687, 398 + i * 81, 705),
                            radius=8, fill=tone if i == st else (43, 82, 100))
    d.text((454, 727), '原票との照合を忘れずに', anchor='mm', font=font(24),
           fill=(175, 205, 215))
    return cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR)


def composite(frame, capture, local_frame, total, genre):
    if frame.shape[:2] != (1920, 1080):
        raise ValueError('invalid source frame size')
    x0, y0, x1, y1 = PANEL
    out = frame.copy()
    out[y0:y1, x0:x1] = panel_image(capture, local_frame, total, genre)
    return out


def render(source, capture, output, manifest, genre='ai_work', window=WINDOW):
    source, capture, output = map(Path, (source, capture, output))
    n = validate(source, capture, output, manifest, genre, window)
    inp = cv2.VideoCapture(str(source))
    cap = cv2.VideoCapture(str(capture))
    ff = subprocess.Popen([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1080x1920',
        '-r', '30', '-i', 'pipe:0', '-i', str(source),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
        '-preset', 'ultrafast', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-c:a', 'copy', '-movflags', '+faststart', str(output)
    ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    edited = 0
    try:
        for idx in range(n):
            ok, frame = inp.read()
            if not ok:
                raise RuntimeError('early source EOF')
            if window[0] <= idx < window[1]:
                ok, shot = cap.read()
                if not ok:
                    raise RuntimeError('early GUI capture EOF')
                frame = composite(frame, shot, idx - window[0],
                                  window[1] - window[0], genre)
                edited += 1
            ff.stdin.write(frame.tobytes())
        ff.stdin.close()
        err = ff.stderr.read().decode(errors='replace')
        if ff.wait() != 0:
            raise RuntimeError('ffmpeg encode failed: ' + err[-1200:])
    except Exception:
        ff.kill(); ff.wait()
        output.unlink(missing_ok=True)
        raise
    finally:
        inp.release(); cap.release()
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output),
                    '-f', 'null', '-'], check=True, stdout=subprocess.DEVNULL)
    v, a = streams(output)
    if int(v['nb_frames']) != n or a['codec_name'] != 'aac':
        raise RuntimeError('A/V output verification failed')
    return {
        'cycle': 851, 'frames': n, 'edited_frames': edited,
        'edit_window': list(window), 'source_sha256': sha256(source),
        'capture_sha256': sha256(capture), 'output_sha256': sha256(output),
        'genre': genre, 'resolution': '1080x1920', 'fps': 30,
        'audio': 'AAC bitstream copied', 'full_av_decode': True,
        'stages': ['不一致を発見', '値を修正', '再計算で一致'],
        'independent_japanese_asr_verified': False,
        'caption_semantic_alignment_verified': False,
        'rights_cleared': False, 'smartphone_playback_verified': False,
        'publication_approved': False,
        'quality_status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    }


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    for key in ('source', 'capture', 'output', 'report'):
        ap.add_argument('--' + key, required=True)
    ap.add_argument('--genre', default='ai_work')
    ap.add_argument('--window', default='422,507')
    a = ap.parse_args()
    s, c = Path(a.source), Path(a.capture)
    w = tuple(map(int, a.window.split(',')))
    report = render(s, c, a.output, {**POLICY, 'source_sha256': sha256(s),
                                     'capture_sha256': sha256(c)}, a.genre, w)
    Path(a.report).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                              encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))