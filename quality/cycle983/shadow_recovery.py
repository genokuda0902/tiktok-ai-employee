"""Cycle983: bounded shadow-detail recovery for captioned vertical slides.

Private media remains local. No rights/approval claim, posting, upload, or merge.
The 10-genre API is shared; only ai_work is layout-reviewed on real footage.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

GENRES = ('ai_work','money','health','science','history','language',
          'career','psychology','travel','lifestyle')
REVIEWED_LAYOUTS = frozenset(('ai_work',))


def validate_geometry(width: int, height: int, fps: float, frames: int,
                      top: int, bottom: int, genre: str, synthetic=False) -> None:
    if genre not in GENRES:
        raise ValueError('Unsupported genre')
    if genre not in REVIEWED_LAYOUTS and not synthetic:
        raise ValueError('Unreviewed real-video layout; fail closed')
    if width < 32 or height < 64 or fps <= 0 or frames < 1:
        raise ValueError('Invalid geometry')
    if not (0 <= top < bottom <= height - 64):
        raise ValueError('Caption safe area must remain untouched')
    if bottom - top < 64:
        raise ValueError('Artwork band too short')


def shadow_lut(strength=22.0, ceiling=160) -> np.ndarray:
    """YCrCb luminance LUT; protects deep black and all highlights."""
    if not (0 <= strength <= 30) or not (100 <= ceiling <= 180):
        raise ValueError('Unsafe tone mapping parameters')
    y = np.arange(256, dtype=np.float32)
    phase = np.clip(y / ceiling, 0, 1)
    lift = strength * np.square(np.maximum(0, np.sin(np.pi * phase)))
    lift[(y < 8) | (y >= ceiling)] = 0
    return np.clip(np.round(y + lift), 0, 255).astype(np.uint8)


def enhance_frame(frame: np.ndarray, top: int, bottom: int,
                  lut: np.ndarray, feather=30) -> np.ndarray:
    if frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
        raise ValueError('Expected uint8 BGR frame')
    h,w = frame.shape[:2]
    if not (0 <= top < bottom <= h-64) or feather < 0 or feather*2 > bottom-top:
        raise ValueError('Invalid protected band')
    out = frame.copy()
    roi = frame[top:bottom]
    ycc = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    source_y = ycc[:,:,0].copy()
    ycc[:,:,0] = cv2.LUT(source_y, lut)
    recovered = cv2.cvtColor(ycc, cv2.COLOR_YCrCb2BGR)
    # Keep highlights and near-black source pixels bit-identical before re-encode.
    mask = (lut[source_y] != source_y)
    recovered[~mask] = roi[~mask]
    if feather:
        fade = np.ones((bottom-top,1,1), dtype=np.float32)
        ramp = np.linspace(0,1,feather,dtype=np.float32)
        fade[:feather,0,0] = ramp
        fade[-feather:,0,0] = ramp[::-1]
        result = np.clip(roi.astype(np.float32)*(1-fade)+recovered.astype(np.float32)*fade,0,255).astype(np.uint8)
        out[top:bottom] = result
    else:
        out[top:bottom] = recovered
    return out


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            digest.update(b)
    return digest.hexdigest()


def render(source: str, output: str, *, genre='ai_work', synthetic=False,
           top=150, bottom=1180, strength=22.0, ceiling=160, feather=0) -> dict:
    src, dst = Path(source), Path(output)
    if src.resolve() == dst.resolve():
        raise ValueError('Never overwrite source')
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise RuntimeError('Source video cannot be opened')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    validate_geometry(width,height,fps,frames,top,bottom,genre,synthetic)
    shadow_lut(strength,ceiling)  # validate bounds; equivalent to FFmpeg YUV LUT
    if feather != 0:
        raise ValueError('FFmpeg fast path requires feather=0; use exact crop boundary')
    dst.parent.mkdir(parents=True,exist_ok=True)
    expression=(f"if(between(val,8,{ceiling}),"
                f"val+{strength}*sin(PI*val/{ceiling})*sin(PI*val/{ceiling}),val)")
    filtergraph=(f"[0:v]split=2[base][tone];"
                 f"[tone]crop=iw:{bottom-top}:0:{top},"
                 f"lutyuv=y='{expression}'[t];"
                 f"[base][t]overlay=0:{top}:shortest=1:format=yuv420[v]")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
         '-filter_complex',filtergraph,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True)
    return {'cycle':983,'source':str(src),'output':str(dst),'genre':genre,
            'width':width,'height':height,'fps':fps,'frames':frames,
            'protected_caption_y_from':bottom,'strength':strength,'ceiling':ceiling,
            'source_sha256':sha256(src),'output_sha256':sha256(dst),
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai_work',choices=GENRES)
    p.add_argument('--synthetic',action='store_true')
    p.add_argument('--top',type=int,default=150)
    p.add_argument('--bottom',type=int,default=1180)
    p.add_argument('--strength',type=float,default=22)
    p.add_argument('--ceiling',type=int,default=160)
    p.add_argument('--feather',type=int,default=0)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,genre=a.genre,synthetic=a.synthetic,
         top=a.top,bottom=a.bottom,strength=a.strength,ceiling=a.ceiling,
         feather=a.feather),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
