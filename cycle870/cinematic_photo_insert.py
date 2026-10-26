"""Review-only image-first photographic scene insert for ten genres.

The photo is an explicitly supplied local image. No external downloads, public
uploads, auto posting or voice generation. Prior Japanese AAC and subtitles are
preserved; approval must be obtained before any publication.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from functools import lru_cache
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

WIDTH, HEIGHT, FPS, FRAME_COUNT = 1080, 1920, 30, 691
SCENE_START, SCENE_FRAMES = 510, 78  # scene 07, 17.0–19.6s
INSERT_TOP, INSERT_BOTTOM = 132, 1490
INSERT_HEIGHT = INSERT_BOTTOM - INSERT_TOP
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': ('使える指示は、資産になる', '目的', '条件', '確認'),
    'sales_business': ('伝わる提案を、資産に', '課題', '提案', '確認'),
    'beauty': ('続けるケアを、習慣に', '目的', '手順', '確認'),
    'romance': ('伝わる会話を、丁寧に', '気持ち', '言葉', '確認'),
    'saving': ('お金の管理を、習慣に', '目標', '記録', '確認'),
    'career': ('学んだことを、実践に', '目標', '行動', '振返'),
    'wellness': ('小さな習慣を、未来に', '目標', '行動', '確認'),
    'science': ('疑問を、発見につなぐ', '疑問', '仮説', '検証'),
    'travel_food': ('旅の計画を、思い出に', '行先', '準備', '確認'),
    'product_comparison_lifestyle': ('選ぶ理由を、明確に', '条件', '比較', '確認'),
}
REVIEW_POLICY = {'review_only': True, 'publication_approved': False,
                 'automatic_posting': False, 'external_upload': False,
                 'source_rights_reviewed': False, 'generated_photo_review_only': True}


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


@lru_cache(maxsize=8)
def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def ease(t):
    t = max(0.0, min(1.0, t))
    return t*t*(3-2*t)


def assert_copy_fits(draw, label, size, x, right):
    if draw.textbbox((x, 0), label, font=font(size))[2] > right:
        raise ValueError(f'text overflows right edge: {label}')


def photo_base(photo):
    if photo.mode not in ('RGB', 'RGBA') or min(photo.size) < 850:
        raise ValueError('photo must be high-resolution RGB or RGBA')
    return ImageEnhance.Contrast(photo.convert('RGB')).enhance(1.08)


def draw_insert_frame(photo, frame: int, genre='ai_work'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 0 <= frame < SCENE_FRAMES:
        raise ValueError('frame out of range')
    photo = photo_base(photo)
    progress = ease(frame / (SCENE_FRAMES - 1))
    # Vertical center crop with a very gentle optical push and slight lateral pan.
    # The generated still is NOT genuine moving camera footage.
    scale = max(WIDTH / photo.width, INSERT_HEIGHT / photo.height) * (1.01 + .055 * progress)
    new_w, new_h = math.ceil(photo.width * scale), math.ceil(photo.height * scale)
    zoomed = photo.resize((new_w, new_h), Image.Resampling.LANCZOS)
    slack_x, slack_y = new_w - WIDTH, new_h - INSERT_HEIGHT
    left = round(slack_x * (.39 + .19 * progress))
    top = round(slack_y * (.49 + .06 * progress))
    left, top = max(0, min(slack_x, left)), max(0, min(slack_y, top))
    frame_im = zoomed.crop((left, top, left + WIDTH, top + INSERT_HEIGHT)).convert('RGBA')
    overlay = Image.new('RGBA', (WIDTH, INSERT_HEIGHT))
    draw = ImageDraw.Draw(overlay, 'RGBA')
    # Glass panel over skyline, separate from inherited Japanese caption strip.
    draw.rounded_rectangle((56, 82, 1024, 293), radius=32,
                           fill=(3, 18, 34, 210), outline=(139, 226, 255, 175), width=3)
    title, *labels = GENRES[genre]
    assert_copy_fits(draw, title, 54, 95, 995)
    draw.text((95, 122), title, font=font(54), fill=(246, 251, 255, 255))
    draw.text((97, 220), 'GOOD PROMPT  /  03', font=font(25), fill=(110, 219, 248, 255))
    # Sequential short copy: use one panel, not multiple nested overlays.
    if frame >= 20:
        draw.rounded_rectangle((63, 1036, 1017, 1210), radius=28,
                               fill=(4, 22, 38, 216), outline=(114, 209, 238, 170), width=3)
        for i, label in enumerate(labels):
            x = 107 + i * 313
            draw.rounded_rectangle((x, 1075, x + 235, 1172), radius=19,
                                   fill=(7, 64, 89, 238) if frame >= 20 + i*15 else (19, 37, 54, 185))
            if frame >= 20 + i*15:
                draw.text((x + 42, 1091), label, font=font(43), fill=(242, 252, 255, 255))
    # An intentionally subtle light leak, drawn separately from text.
    light = Image.new('RGBA', (WIDTH, INSERT_HEIGHT))
    glow = ImageDraw.Draw(light, 'RGBA')
    cx = 100 + int(progress * 80)
    glow.ellipse((cx-130, 600, cx+130, 920), fill=(255, 191, 97, 24))
    light = light.filter(ImageFilter.GaussianBlur(55))
    return Image.alpha_composite(Image.alpha_composite(frame_im, light), overlay).convert('RGB')


def probe(path):
    obj = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                                               '-of','json',str(path)], text=True))
    v = next(x for x in obj['streams'] if x['codec_type'] == 'video')
    a = next(x for x in obj['streams'] if x['codec_type'] == 'audio')
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate'],
        int(v['nb_frames']), a['codec_name'], a['sample_rate']) != (
        'h264', WIDTH, HEIGHT, '30/1', FRAME_COUNT, 'aac', '48000'):
        raise ValueError('invalid media specification')
    return {'video_codec': v['codec_name'], 'width': v['width'], 'height': v['height'],
            'fps': v['r_frame_rate'], 'frames': int(v['nb_frames']),
            'audio_codec': a['codec_name'], 'audio_sample_rate': int(a['sample_rate'])}


def render(source, photo_path, output, manifest, genre='ai_work'):
    source, photo_path, output = map(Path, (source, photo_path, output))
    if genre not in GENRES or not source.is_file() or not photo_path.is_file():
        raise ValueError('missing source/photo or unsupported genre')
    if output.exists() or source.resolve() == output.resolve():
        raise ValueError('refusing to overwrite existing video')
    expected = {**REVIEW_POLICY, 'source_sha256': sha256(source),
                'photo_sha256': sha256(photo_path)}
    if manifest != expected:
        raise ValueError('source/photo provenance or review-only gate rejected')
    probe(source)
    with Image.open(photo_path) as src_photo:
        img = src_photo.copy()
    with tempfile.TemporaryDirectory(prefix='cycle870_') as td:
        td = Path(td)
        for i in range(SCENE_FRAMES):
            draw_insert_frame(img, i, genre).save(td / f'{i:03d}.jpg',
                                                  quality=92, subsampling=0)
        # Overlay only central image region. Existing title, subtitles and AAC retained.
        filt = (f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{SCENE_START}/(30*TB)[new];'
                f'[0:v][new]overlay=x=0:y={INSERT_TOP}:'
                f"enable='between(n,{SCENE_START},{SCENE_START+SCENE_FRAMES-1})':"
                'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd = ['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
               '-framerate','30','-start_number','0','-i',str(td / '%03d.jpg'),
               '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
               '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30',
               '-frames:v',str(FRAME_COUNT),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd, check=True, timeout=240)
    spec = probe(output)
    return {'input_sha256': sha256(source), 'photo_sha256': sha256(photo_path),
            'output_sha256': sha256(output), 'frame_range': [SCENE_START,SCENE_START+SCENE_FRAMES-1],
            'changed_frames': SCENE_FRAMES, 'genre': genre, 'genres_supported': len(GENRES),
            'media': spec, 'policy': REVIEW_POLICY}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    for name in ('source','photo','output','manifest','report'):
        p.add_argument('--'+name, required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    report=render(a.source,a.photo,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))