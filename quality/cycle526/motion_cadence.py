#!/usr/bin/env python3
"""Genre-neutral progressive-focus overlay for REVIEW_ONLY portrait MP4s.

Reimplementation, not original v33. No external assets or API requests.
The existing audio is copied without modifying it; Japanese narration is NOT asserted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw

W, H, FPS = 1080, 1920, 30
GENRES = ('ai_work', 'beauty', 'relationship', 'money', 'sales', 'career', 'health', 'science', 'travel', 'products')

@dataclass(frozen=True)
class FocusScene:
    start: float
    end: float
    boxes: tuple[tuple[int, int, int, int], ...]

DEMO = FocusScene(2.5, 4.0, ((44, 540, 885, 690), (44, 720, 885, 870), (44, 900, 885, 1050)))


def validate(manifest: dict, scene: FocusScene) -> None:
    if manifest.get('genre') not in GENRES:
        raise ValueError('unknown genre')
    if manifest.get('rights') != 'synthetic_local_review_only' or manifest.get('privacy_checked') is not True:
        raise ValueError('asset rights/privacy gate')
    if manifest.get('publication') != 'NOT_APPROVED' or manifest.get('human_review') != 'HUMAN_REVIEW' or manifest.get('auto_post') is not False:
        raise ValueError('publication gate')
    if not (0 <= scene.start < scene.end <= 20 and 0.5 <= scene.end-scene.start <= 6):
        raise ValueError('invalid scene timing')
    if scene.end > float(manifest.get('scene_cut_seconds', scene.end)):
        raise ValueError('overlay crosses scene cut')
    if not (2 <= len(scene.boxes) <= 6):
        raise ValueError('scene needs 2-6 focus boxes')
    for x0, y0, x1, y1 in scene.boxes:
        if not (24 <= x0 < x1 <= 940 and 180 <= y0 < y1 <= 1500 and x1-x0 >= 160 and y1-y0 >= 60):
            raise ValueError('box outside content safe-zone')
    for i, (x0, y0, x1, y1) in enumerate(scene.boxes):
        for xx0, yy0, xx1, yy1 in scene.boxes[i+1:]:
            if max(x0, xx0) < min(x1, xx1) and max(y0, yy0) < min(y1, yy1):
                raise ValueError('focus boxes overlap')


def stage_at(t: float, scene: FocusScene) -> tuple[int, float]:
    if not scene.start <= t < scene.end:
        raise ValueError('outside scene')
    n = len(scene.boxes)
    active_end = scene.end - 0.20
    if t >= active_end:
        return n, 1.0
    u = (t-scene.start)/(active_end-scene.start)*n
    return min(n-1, int(u)), u-math.floor(u)


def draw_frame(scene: FocusScene, t: float) -> Image.Image:
    # Render at half resolution; the FFmpeg compositor scales to 1080x1920.
    im = Image.new('RGBA', (W//2, H//2), (0,0,0,0))
    d = ImageDraw.Draw(im, 'RGBA')
    idx, phase = stage_at(t, scene)
    for j, (x0,y0,x1,y1) in enumerate(scene.boxes):
        box = tuple(round(v/2) for v in (x0,y0,x1,y1))
        if idx < len(scene.boxes) and j != idx:
            d.rounded_rectangle(box, radius=14, fill=(0,8,20,75))
            continue
        if idx == len(scene.boxes):
            line_color = (61,225,185,165)
            progress = 1.0
        else:
            pulse = (1 + math.sin(phase*math.pi*2))/2
            line_color = (255,213,101, int(175+65*pulse))
            progress = phase
        for inset, alpha, width in ((-8,38,6), (-3,75,4), (2,210,3)):
            b=(box[0]+inset,box[1]+inset,box[2]-inset,box[3]-inset)
            if b[2]>b[0] and b[3]>b[1]:
                d.rounded_rectangle(b,radius=14,outline=(*line_color[:3],alpha),width=width)
        d.rounded_rectangle((box[0]+3,box[3]-9,box[0]+3+int((box[2]-box[0]-6)*progress),box[3]-4),radius=2,fill=line_color)
        # Small, high-contrast marker outside the content text.
        d.ellipse((box[2]-23,box[1]+6,box[2]-8,box[1]+21),fill=line_color)
    return im


def run(cmd: list[str]) -> str:
    p=subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f'{cmd[0]} failed ({p.returncode}): {p.stderr[-3000:]}')
    return p.stdout


def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,sample_rate','-of','json',str(path)]))


def render(source: Path, target: Path, scene: FocusScene, manifest: dict, workdir: Path) -> dict:
    validate(manifest, scene)
    if not source.is_file():
        raise FileNotFoundError(source)
    meta=probe(source)
    vid=next((s for s in meta['streams'] if s['codec_type']=='video'),{})
    aud=next((s for s in meta['streams'] if s['codec_type']=='audio'),{})
    if vid.get('width') != W or vid.get('height') != H or vid.get('codec_name') != 'h264' or aud.get('codec_name') != 'aac':
        raise ValueError('source codec or geometry gate')
    if abs(float(meta['format']['duration'])-20.0)>0.1:
        raise ValueError('source duration gate')
    workdir.mkdir(parents=True, exist_ok=True)
    frames=int(round((scene.end-scene.start)*FPS))
    for n in range(frames):
        draw_frame(scene, scene.start+n/FPS).save(workdir/f'overlay_{n:03d}.png',optimize=True)
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(source),'-framerate',str(FPS),'-i',str(workdir/'overlay_%03d.png'),
         '-filter_complex',f'[1:v]format=rgba,scale={W}:{H},setpts=PTS+{scene.start}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:format=auto[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart','-t','20',str(target)]
    run(cmd)
    new=probe(target)
    if abs(float(new['format']['duration'])-20.0)>0.1:
        raise ValueError('render duration gate')
    return {'source':str(source),'output':str(target),'frames':frames,'genre':manifest['genre'],
            'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'publication':'NOT_APPROVED','voice':'NOT_VERIFIED'}


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--workdir',type=Path,required=True)
    args=ap.parse_args();manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
    print(json.dumps(render(args.source,args.output,DEMO,manifest,args.workdir),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
