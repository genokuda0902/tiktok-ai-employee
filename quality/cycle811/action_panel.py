#!/usr/bin/env python3
"""cycle811: opaque, non-overlapping action-card renderer; review-only.

Repairs inherited cycle810 scene-six ghosting without changing the other seven
scenes, the narration, or the original on-screen subtitle. All ten genres share
one safe layout. Never uploads private source media or posts to TikTok.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FRAMES = 718
START = 445
SCENE = 94
PW, PH = 850, 600
X, Y = 115, 730
AUTO_POST = False
EMPLOYEE_APPROVAL = False
# These are example instructions, not a representation of actual staff actions.
GENRES = {
    'ai_work': ('担当を決める', '手順を１つ試す', '今日中に確認'),
    'beauty': ('担当を決める', '手順を１つ試す', '今日中に確認'),
    'love_psychology': ('担当を決める', '伝え方を試す', '今日中に確認'),
    'money_saving': ('担当を決める', '予算を１つ見直す', '今日中に確認'),
    'sales_business': ('担当を決める', '改善を１つ試す', '今日中に振り返る'),
    'career': ('担当を決める', '学習を１つ試す', '今日中に確認'),
    'health_life': ('担当を決める', '習慣を１つ試す', '今日中に確認'),
    'science': ('担当を決める', '仮説を１つ試す', '今日中に確認'),
    'travel_food': ('担当を決める', '計画を１つ試す', '今日中に確認'),
    'product_life': ('担当を決める', '使い方を試す', '今日中に確認'),
}
LABELS = ('誰が', '何を', 'いつまで')
FONT_PATHS = (
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
)

def font(size):
    p = os.getenv('CYCLE811_FONT') or next((f for f in FONT_PATHS if Path(f).is_file()), None)
    if not p:
        raise RuntimeError('Japanese font unavailable; set CYCLE811_FONT')
    return ImageFont.truetype(p, size)

def validate(genre):
    if genre not in GENRES:
        raise ValueError('Unsupported genre')
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for s in GENRES[genre]:
        if any(c in s for c in '\r\n\x00'):
            raise ValueError('Unsafe text')
        box = d.textbbox((0, 0), s, font=font(47))
        if box[2] - box[0] > 525:
            raise ValueError('Text exceeds safe action-card width')
    return GENRES[genre]

def panel_frame(i, genre='sales_business'):
    if not 0 <= i < SCENE:
        raise ValueError('Invalid scene frame')
    values = validate(genre)
    # RGB, not translucent RGBA: fully erases previously ghosted text.
    im = Image.new('RGB', (PW, PH), '#071c2b')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((5, 5, PW-5, PH-5), radius=32, fill='#092235', outline='#73bec7', width=3)
    d.rounded_rectangle((25, 24, PW-25, 108), radius=21, fill='#19475a')
    d.text((49, 38), 'TODAY / ACTION PLAN', font=font(35), fill='#effcff')
    d.text((663, 47), '行動例', font=font(30), fill='#ffe1a4')
    active = min(3, 1 + (i >= 29) + (i >= 57))
    for j, (label, value) in enumerate(zip(LABELS, values)):
        top = 133 + 126*j
        visible = j < active
        fill = '#173d50' if visible else '#0e2939'
        outline = '#7ae1d4' if visible else '#2c5160'
        d.rounded_rectangle((30, top, 820, top+104), radius=21, fill=fill, outline=outline, width=3)
        d.ellipse((46, top+24, 103, top+81), fill='#55d9c8' if visible else '#24495b')
        d.text((65, top+32), str(j+1), font=font(29), fill='#092235' if visible else '#b2c6d0')
        d.text((118, top+31), label, font=font(33), fill='#c8e5e9' if visible else '#6d8995')
        if visible:
            d.text((300, top+21), value, font=font(47), fill='#ffffff')
            d.text((748, top+24), '✓', font=font(49), fill='#68ebd4')
        else:
            d.text((322, top+32), '―', font=font(36), fill='#6d8995')
    d.rounded_rectangle((32, 551, 818, 566), radius=7, fill='#234859')
    d.rounded_rectangle((32, 551, 32+round(786*(active/3)), 566), radius=7, fill='#61d8c9')
    return im

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def probe(path):
    p = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)], check=True, capture_output=True, text=True)
    return json.loads(p.stdout)

def render(source, output, genre='sales_business'):
    validate(genre)
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle811_') as td:
        td = Path(td)
        for i in range(SCENE):
            panel_frame(i, genre).save(td/f'{i:03}.png')
        # Frame-exact start: 445 / 30 s. The source audio is stream-copied.
        filtergraph = (f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/{FPS}/TB[panel];'
                       f'[0:v][panel]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:format=auto[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-i',str(source),'-framerate',str(FPS),'-start_number','0',
             '-i',str(td/'%03d.png'),'-filter_complex',filtergraph,
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','20','-pix_fmt','yuv420p','-frames:v',str(FRAMES),
             '-c:a','copy','-movflags','+faststart',str(output)])
    meta = probe(output)
    vs = next(s for s in meta['streams'] if s['codec_type']=='video')
    au = next(s for s in meta['streams'] if s['codec_type']=='audio')
    assert (vs['width'],vs['height'],vs['avg_frame_rate']) == (W,H,'30/1')
    assert au['codec_name']=='aac' and au['sample_rate']=='48000'
    assert abs(float(meta['format']['duration']) - FRAMES/FPS) < 0.06
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    qa = dict(genre=genre, frames=FRAMES, start_frame=START, scene_frames=SCENE,
              width=W, height=H, fps=FPS, audio_codec='aac',
              source_audio_copied=True, japanese_voice_content_verified=False,
              caption_semantics_verified=False, publication_approved=False,
              auto_post=False, private_review_only=True,
              output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    (output.parent/'cycle811_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='sales_business',choices=tuple(GENRES))
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
