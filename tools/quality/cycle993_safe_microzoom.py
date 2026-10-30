#!/usr/bin/env python3
"""Safe-area micro camera movement for image-first vertical shorts.

Changes only a feather-masked content ROI. Title, baked Japanese subtitle,
footer and TikTok overlay-safe regions remain untouched before re-encoding.
Does not create speech, change timing, grant content rights or approve posting.
All genre presets share one renderer; adjust ROI for each new template.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

GENRE_ZOOM = {
    'ai_work': .018, 'business': .014, 'finance': .012,
    'education': .016, 'health': .012, 'travel': .022,
    'cooking': .022, 'lifestyle': .020, 'technology': .016,
    'entertainment': .022,
}

def eased_zoom(frame: int, scene_frames: int = 87, strength: float = .018) -> float:
    import math
    if scene_frames < 3 or not 0 <= strength <= .04:
        raise ValueError('invalid zoom settings')
    phase = (frame % scene_frames) / (scene_frames - 1)
    return 1 + strength * (.5 - .5 * math.cos(2 * math.pi * phase))

def feather_mask(path: Path, w: int, h: int, feather: int = 42) -> None:
    if min(w, h) <= feather * 2 or feather < 2:
        raise ValueError('feather too large or too small')
    def smooth(v: float) -> float:
        v = max(0., min(1., v))
        return v*v*(3-2*v)
    ax = [smooth(min(x, w-1-x)/feather) for x in range(w)]
    ay = [smooth(min(y, h-1-y)/feather) for y in range(h)]
    mask = Image.new('L', (w,h))
    mask.putdata([round(255*min(ax[x],ay[y])) for y in range(h) for x in range(w)])
    mask.save(path)

def filter_graph(x: int, y: int, w: int, h: int,
                 scene_frames: int, strength: float) -> str:
    if min(x,y,w,h) < 0 or w <= 0 or h <= 0 or scene_frames < 3:
        raise ValueError('invalid geometry')
    if not 0 <= strength <= .04:
        raise ValueError('strength out of range')
    zoom = (f"1+{strength:.5f}*(0.5-0.5*cos(2*PI*mod(on,{scene_frames})/"
            f"{scene_frames-1}))")
    return (f"[0:v]split=2[base][detail];"
            f"[detail]crop={w}:{h}:{x}:{y},"
            f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2':"
            f"y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps=30,format=rgb24[zoomed];"
            f"[1:v]format=gray[mask];[zoomed][mask]alphamerge[soft];"
            f"[base][soft]overlay={x}:{y}:shortest=1:format=auto,format=yuv420p[v]")

def render(src: Path, dst: Path, *, genre: str = 'ai_work',
           roi=(90,300,900,850), scene_frames: int = 87,
           feather: int = 42, seconds: float | None = None) -> None:
    if genre not in GENRE_ZOOM:
        raise ValueError('unknown genre')
    if not src.is_file():
        raise FileNotFoundError(src)
    x,y,w,h = roi
    if x < 0 or y < 0 or x+w > 1080 or y+h > 1190:
        raise ValueError('ROI must avoid subtitle/footer and stay in 1080x1920 frame')
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        mask = Path(tmp)/'feather.png'
        feather_mask(mask,w,h,feather)
        cmd = ['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(src),
               '-loop','1','-framerate','30','-i',str(mask),
               '-filter_complex',filter_graph(x,y,w,h,scene_frames,GENRE_ZOOM[genre]),
               '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
               '-crf','19','-pix_fmt','yuv420p','-c:a','copy',
               '-movflags','+faststart']
        if seconds is not None:
            cmd.extend(['-t',str(seconds)])
        cmd.append(str(dst))
        subprocess.run(cmd,check=True)

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--genre',choices=GENRE_ZOOM,default='ai_work')
    p.add_argument('--scene-frames',type=int,default=87)
    p.add_argument('--seconds',type=float,default=None)
    args=p.parse_args()
    render(args.input,args.output,genre=args.genre,
           scene_frames=args.scene_frames,seconds=args.seconds)

if __name__=='__main__': main()
