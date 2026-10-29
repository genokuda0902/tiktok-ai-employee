"""Review-only artwork-region midtone lift for image-first TikTok videos."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

REVIEWED_SHA256 = "c9b4680679977fdf20d139d9106e4ca219fad267595f005f3eb6e00e48a3414d"
GENRE_GAMMA = {
    "ai_work": 1.14, "business": 1.12, "finance": 1.10,
    "education": 1.12, "career": 1.13, "wellness": 1.11,
    "lifestyle": 1.12, "technology": 1.14, "travel": 1.11,
    "trivia": 1.12,
}
WIDTH, HEIGHT = 1080, 1920
ART_BOUNDS = (48, 420, 1032, 1290)
FEATHER = 70

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def mask_array(width: int = WIDTH, height: int = HEIGHT, bounds=ART_BOUNDS,
               feather: int = FEATHER) -> np.ndarray:
    """Cosine edge taper; preserve top labels and burned subtitle bands."""
    x0, y0, x1, y1 = bounds
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError('invalid artwork bounds')
    if feather <= 0 or feather * 2 >= min(x1-x0, y1-y0):
        raise ValueError('invalid feather')
    xs = np.arange(width, dtype=np.float32)
    ys = np.arange(height, dtype=np.float32)
    def ramp(v, low, high):
        dist = np.minimum(v-low, high-1-v)
        z = np.clip(dist / feather, 0, 1)
        return 0.5 - 0.5 * np.cos(np.pi * z)
    m = np.outer(ramp(ys, y0, y1), ramp(xs, x0, x1))
    return np.rint(255*m).astype(np.uint8)

def render(source: Path, output: Path, genre: str = 'ai_work',
           mask_path: Path | None = None, *, expected_sha: str = REVIEWED_SHA256) -> dict:
    if genre not in GENRE_GAMMA:
        raise ValueError('unknown genre')
    digest = sha256(source)
    if digest != expected_sha or genre != 'ai_work':
        raise PermissionError('unreviewed source/genre; fail closed')
    output.parent.mkdir(parents=True, exist_ok=True)
    mask_path = mask_path or output.with_suffix('.mask.png')
    Image.fromarray(mask_array(), 'L').save(mask_path)
    gamma = GENRE_GAMMA[genre]
    filter_graph = (
        '[0:v]split=2[original][work];'
        f'[work]eq=gamma={gamma}:gamma_weight=0.82[graded];'
        '[original][graded][1:v]maskedmerge=planes=0x7,format=yuv420p[v]'
    )
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
           '-loop','1','-framerate','30','-i',str(mask_path),
           '-filter_complex',filter_graph,'-map','[v]','-map','0:a:0',
           '-frames:v','691','-c:v','libx264','-preset','veryfast','-crf','18',
           '-pix_fmt','yuv420p','-c:a','copy',
           '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
           '-movflags','+faststart','-metadata:s:a:0','language=jpn',str(output)]
    subprocess.run(cmd, check=True, timeout=240)
    return {'input_sha256':digest,'output_sha256':sha256(output),'genre':genre,
            'gamma':gamma,'mask':str(mask_path),'output':str(output),
            'review_only':True,'publication_approved':False,'command':cmd}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--genre',default='ai_work')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
