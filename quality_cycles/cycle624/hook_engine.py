#!/usr/bin/env python3
"""Zero-cost, mobile-first two-beat hook for existing vertical image-slide videos.

Only modifies the FIRST SCENE's heading and a small underline; preserves
all original audio packets and all non-hook scene content. Does not claim
voice/transcript alignment or grant permission to publish inherited imagery.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
HEADER = (45, 182, 890, 350)
FIRST_SCENE_END = 70
BREAK = 28

def _hex_rgb(code):
    return tuple(bytes.fromhex(code.lstrip('#')))

def make_overlay(beat, accent, progress):
    """Build one small alpha overlay; no changes to the hero/subtitle areas."""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, 'RGBA')
    d.rounded_rectangle(HEADER, radius=10, fill=(5, 15, 29, 255))
    text = beat['text']
    ft = ImageFont.truetype(FONT, 74 if len(text) <= 10 else 65)
    bb = d.textbbox((0, 0), text, font=ft)
    width = bb[2] - bb[0]
    if width > 800:
        ft = ImageFont.truetype(FONT, int(ft.size * 800 / width))
        bb = d.textbbox((0, 0), text, font=ft)
        width = bb[2] - bb[0]
    x = 54
    y = 202
    d.text((x, y), text, font=ft, fill=(255, 255, 255, 255), stroke_width=0)
    rgb = _hex_rgb(accent)
    d.rounded_rectangle((x, 321, x + int(700 * progress), 331), radius=5, fill=(*rgb, 240))
    return np.asarray(img)

def render(source, output, hooks, genre):
    source, output = Path(source), Path(output)
    profile = hooks['genres'][genre]
    if len(hooks['genres']) != 10:
        raise ValueError('Expected 10 genre profiles')
    cap = cv2.VideoCapture(str(source))
    dims = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(cap.get(cv2.CAP_PROP_FPS)),
            int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    if dims != (W, H, FPS, 468):
        cap.release()
        raise ValueError(f'Unexpected source geometry: {dims}')
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}',
           '-r',str(FPS),'-i','pipe:0','-i',str(source),
           '-map','0:v:0','-map','1:a:0','-c:v','libx264',
           '-preset','veryfast','-crf','18','-threads','2',
           '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    count = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok: break
            if count < FIRST_SCENE_END:
                index = 0 if count < BREAK else 1
                local = count if index == 0 else count - BREAK
                duration = BREAK if index == 0 else FIRST_SCENE_END - BREAK
                progress = min(1, (local + 1) / max(1, duration))
                overlay = make_overlay(profile['beats'][index], profile['accent'], progress)
                alpha = overlay[...,3:4].astype(np.float32) / 255
                bgr = overlay[...,:3][:,:,::-1]
                frame = np.clip(frame.astype(np.float32) * (1 - alpha) + bgr * alpha, 0, 255).astype(np.uint8)
            p.stdin.write(frame.tobytes())
            count += 1
        p.stdin.close()
        err = p.stderr.read().decode(errors='replace')
        if p.wait(): raise RuntimeError(f'ffmpeg: {err[-1200:]}')
    finally:
        cap.release()
        if p.poll() is None: p.kill()
    if count != 468: raise RuntimeError(f'Unexpected output frame count {count}')
    return {'frames':count,'modified_frames':FIRST_SCENE_END,'beat_change_frame':BREAK,
            'genre':genre,'profiles':len(hooks['genres']),
            'publication':'NOT_APPROVED','status':'HUMAN_REVIEW'}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--hooks',type=Path,default=Path(__file__).with_name('hooks.json'))
    ap.add_argument('--genre',default='雑学・科学')
    a=ap.parse_args()
    print(json.dumps(render(a.input,a.output,json.loads(a.hooks.read_text(encoding='utf-8')),a.genre),ensure_ascii=False,indent=2))
