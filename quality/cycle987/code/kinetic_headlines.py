#!/usr/bin/env python3
"""Cycle987: caption-safe kinetic chapter headlines for a private review MP4.

The overlay changes only x=40..700, y=188..335, with a narrow legacy-title
feather x=660..775 y=190..281. The source AAC stream is copied unchanged.
All non-AI-work genres fail closed for real footage until layout review.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_BOUNDARIES = (0, 87, 174, 261, 348, 435, 522, 609, 691)
CAPTION_SAFE_Y = 1180
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
TITLES = (
    'AIで仕事を速くする',
    '繰り返す作業を書き出す',
    '完成形の見本を用意',
    '目的と条件を具体的に',
    'AIの出力を自分で確認',
    '修正は1つずつ伝える',
    '使える指示を保存',
    '小さな時短を習慣に',
)
GENRES = {
    'ai_work': (38, 229, 211),
    'trivia': (252, 194, 71),
    'cooking': (251, 134, 87),
    'beauty': (245, 150, 183),
    'finance': (113, 213, 133),
    'health': (116, 209, 211),
    'travel': (111, 177, 250),
    'products': (185, 152, 247),
    'story': (246, 121, 132),
    'career': (239, 190, 106),
}

@dataclass(frozen=True)
class Layout:
    x: int = 40
    y: int = 188
    w: int = 660
    h: int = 147
    text_x: int = 69
    text_y: int = 251
    line_y: int = 320

LAYOUT = Layout()

def ease_out_cubic(v: float) -> float:
    v = max(0.0, min(1.0, v))
    return 1 - (1 - v) ** 3

def scene_for_frame(frame: int, boundaries=SCENE_BOUNDARIES):
    for i in range(len(boundaries) - 1):
        if boundaries[i] <= frame < boundaries[i + 1]:
            return i, frame - boundaries[i]
    raise ValueError(f'frame {frame} outside {boundaries[-1]} frames')

def font(path: str, size: int):
    if not Path(path).exists():
        raise FileNotFoundError(f'Japanese font missing: {path}')
    return ImageFont.truetype(path, size)

def make_card(accent: tuple[int,int,int], title: str):
    w, h = LAYOUT.w, LAYOUT.h
    panel = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    d.rounded_rectangle((1, 1, w-2, h-2), radius=19,
                        fill=(3, 14, 37, 249), outline=(*accent, 158), width=2)
    d.rounded_rectangle((10, 16, 16, h-16), radius=3, fill=(*accent, 235))
    d.text((29, 10), 'KEY IDEA  /  今日のポイント', font=font(FONT_REGULAR, 17),
           fill=(*accent, 236))
    label = Image.new('RGBA', (w, h), (0,0,0,0))
    ld = ImageDraw.Draw(label)
    fs = 50
    while font(FONT_BOLD, fs).getlength(title) > 565 and fs > 36:
        fs -= 1
    ld.text((LAYOUT.text_x-LAYOUT.x, LAYOUT.text_y-LAYOUT.y), title,
            font=font(FONT_BOLD, fs), fill=(246,249,255,255), stroke_width=0)
    return np.asarray(panel).copy(), np.asarray(label).copy(), fs

def alpha_over(base: np.ndarray, rgba: np.ndarray, x: int, y: int):
    h,w=rgba.shape[:2]
    if x<0 or y<0 or x+w>base.shape[1] or y+h>base.shape[0]:
        raise ValueError('Overlay outside frame')
    roi=base[y:y+h,x:x+w]
    alpha=rgba[:,:,3:4].astype(np.float32)/255.0
    bgr=rgba[:,:,:3][:,:,::-1].astype(np.float32)
    roi[:]=np.clip(roi.astype(np.float32)*(1-alpha)+bgr*alpha,0,255).astype(np.uint8)

def render_frame(frame: np.ndarray, index: int, cards, accent=(38,229,211), boundaries=SCENE_BOUNDARIES):
    if frame.shape[:2] != (HEIGHT,WIDTH):
        raise ValueError(f'expected 1080x1920, got {frame.shape}')
    scene, local = scene_for_frame(index, boundaries)
    card, label, _ = cards[scene]
    # Feather long original Japanese title tails above the right-hand chip.
    tail=frame[190:281, 660:775]
    ramp=np.concatenate((np.full(80,0.995,dtype=np.float32),
                         np.linspace(0.995,0.0,tail.shape[1]-80,dtype=np.float32)))[None,:,None]
    tail[:]=np.clip(tail.astype(np.float32)*(1-ramp)+
                    np.array([37,14,3],dtype=np.float32)*ramp,0,255).astype(np.uint8)
    alpha_over(frame, card, LAYOUT.x, LAYOUT.y)
    reveal=ease_out_cubic(local/14.0)
    visible=max(0,min(LAYOUT.w, int(LAYOUT.w*reveal)))
    if visible:
        alpha_over(frame, label[:, :visible, :], LAYOUT.x, LAYOUT.y)
    line=ease_out_cubic((local-5)/19.0)
    start=LAYOUT.text_x
    end=start+int(500*line)
    if end>start:
        cv2.line(frame, (start,LAYOUT.line_y),(end,LAYOUT.line_y),
                 (accent[2],accent[1],accent[0]),3,cv2.LINE_AA)
    if local<14:
        cx=min(LAYOUT.x+LAYOUT.w-15,LAYOUT.x+visible+3)
        cv2.line(frame,(cx,LAYOUT.text_y+6),(cx,LAYOUT.text_y+51),
                 (accent[2],accent[1],accent[0]),2,cv2.LINE_AA)
    return frame

def run(source: Path, output: Path, genre: str, synthetic=False, titles_json=None, max_frames=None):
    if genre not in GENRES:
        raise ValueError(f'Unknown genre {genre}')
    if not synthetic and genre!='ai_work':
        raise ValueError('Non-AI-work footage requires manual layout approval')
    titles=list(TITLES)
    if titles_json:
        titles=json.loads(Path(titles_json).read_text(encoding='utf-8'))
        if len(titles)!=8 or not all(isinstance(t,str) and t.strip() for t in titles):
            raise ValueError('titles JSON must contain eight nonempty strings')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise FileNotFoundError(source)
    fps=cap.get(cv2.CAP_PROP_FPS)
    w,h=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (w,h)!=(WIDTH,HEIGHT) or abs(fps-FPS)>0.01:
        raise ValueError(f'expected 1080x1920 30fps; got {w}x{h} {fps}')
    if not synthetic and total!=691:
        raise ValueError(f'real review layout locked to 691 frames, got {total}')
    n=total if max_frames is None else min(max_frames,total)
    if synthetic:
        boundaries=tuple(int(round(i*n/8)) for i in range(9))
        if len(set(boundaries))<9:
            raise ValueError('synthetic test requires at least 8 frames')
    else:
        boundaries=SCENE_BOUNDARIES
    cards=[make_card(GENRES[genre],t) for t in titles]
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s',f'{WIDTH}x{HEIGHT}',
         '-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264',
         '-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-frames:v',str(n),'-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0
    try:
        while count<n:
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'input ended after {count} frames')
            render_frame(frame,count,cards,GENRES[genre],boundaries)
            proc.stdin.write(frame.tobytes())
            count+=1
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8',errors='replace')
        rc=proc.wait()
        if rc: raise RuntimeError(f'ffmpeg exit {rc}: {err[-1500:]}')
    except Exception:
        if proc.poll() is None: proc.kill()
        raise
    finally:
        cap.release()
    return {'frames':count,'genre':genre,'titles':titles,'source':str(source),'output':str(output)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    p.add_argument('--titles-json')
    p.add_argument('--max-frames',type=int)
    args=p.parse_args()
    print(json.dumps(run(args.source,args.output,args.genre,args.synthetic,args.titles_json,args.max_frames),ensure_ascii=False))

if __name__=='__main__': main()
