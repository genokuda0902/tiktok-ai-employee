"""cycle620: genre-neutral temporal caption-safe loop bridge (review only).

Unlike spatial wipe, every frame is a whole-image uniform-opacity transition:
CTA -> solid slate -> opening. This prevents captions being sliced at a moving
wipe boundary. Does NOT generate or claim Japanese speech; inherited media rights
remain unverified. Requires approved rights before publication. No network/post.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from PIL import Image

GENRES = {
    'ai_work': 'AI・仕事効率化',
    'beauty': '美容・身だしなみ',
    'relationships': '恋愛・心理',
    'money': 'お金・節約',
    'sales_business': '営業・ビジネス',
    'career': '転職・キャリア',
    'health_lifestyle': '健康・生活改善',
    'science_trivia': '雑学・科学',
    'travel_food': '旅行・グルメ',
    'product_lifestyle': '商品比較・暮らし',
}

@dataclass(frozen=True)
class BridgeSpec:
    genre: str = 'ai_work'
    frames: int = 27
    fps: int = 30
    slate_rgb: tuple[int, int, int] = (7, 22, 38)
    publication_status: str = 'NOT_APPROVED'

    def validate(self) -> None:
        if self.genre not in GENRES:
            raise ValueError('Unknown genre')
        if self.fps != 30 or not 18 <= self.frames <= 45 or self.frames % 2 != 1:
            raise ValueError('Requires 0.6-1.5 seconds, 30fps, odd frame count')
        if len(self.slate_rgb) != 3 or any(not 0 <= c <= 255 for c in self.slate_rgb):
            raise ValueError('Invalid slate RGB')
        if self.publication_status != 'NOT_APPROVED':
            raise ValueError('Human approval required')

def smoothstep(t: float) -> float:
    if not 0 <= t <= 1:
        raise ValueError('Invalid progress')
    return t * t * (3 - 2 * t)

def blend_whole(a: np.ndarray, b: np.ndarray, opacity: float) -> np.ndarray:
    """Global scalar opacity; never spatially splits a glyph."""
    if a.shape != b.shape or a.ndim != 3 or a.shape[2] != 3 or a.dtype != np.uint8 or b.dtype != np.uint8:
        raise ValueError('Equal-sized RGB uint8 frames required')
    if not 0 <= opacity <= 1:
        raise ValueError('Opacity outside 0..1')
    if opacity == 0:
        return a.copy()
    if opacity == 1:
        return b.copy()
    return np.rint(a.astype(np.float32)*(1-opacity)+b.astype(np.float32)*opacity).astype(np.uint8)

def bridge_frame(tail: np.ndarray, opening: np.ndarray, index: int, spec: BridgeSpec) -> np.ndarray:
    spec.validate()
    if not 0 <= index < spec.frames:
        raise ValueError('Frame index out of bounds')
    slate = np.empty_like(tail)
    slate[:] = spec.slate_rgb
    half = (spec.frames-1)//2
    if index <= half:
        return blend_whole(tail, slate, smoothstep(index/half))
    return blend_whole(slate, opening, smoothstep((index-half)/half))

def command(argv: list[str], logfile: Path) -> str:
    proc = subprocess.run(argv, text=True, capture_output=True)
    with logfile.open('a', encoding='utf8') as f:
        f.write(' '.join(argv)+'\n'+proc.stdout+proc.stderr+'\n')
    if proc.returncode:
        raise RuntimeError(f'Command exit {proc.returncode}: {argv[0]}: {proc.stderr[-900:]}')
    return proc.stdout

def probe(path: Path, log: Path) -> dict:
    return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],log))

def render(baseline: Path, output: Path, work: Path, spec: BridgeSpec = BridgeSpec()) -> dict:
    spec.validate()
    work.mkdir(parents=True, exist_ok=True)
    log = work/'commands.log'; log.write_text('', encoding='utf8')
    meta = probe(baseline, log)
    v = next(s for s in meta['streams'] if s['codec_type']=='video')
    audio = next((s for s in meta['streams'] if s['codec_type']=='audio'),None)
    if v['codec_name']!='h264' or (v['width'],v['height'])!=(1080,1920) or not audio:
        raise ValueError('Baseline must be H.264 1080x1920 with audio')
    fps = v['r_frame_rate'].split('/')
    if abs(int(fps[0])/int(fps[1])-spec.fps)>0.001:
        raise ValueError('Expected 30 fps')
    n = int(v['nb_frames'])
    if n < spec.frames+10:
        raise ValueError('Video too short')
    first = work/'opening.png'
    command(['ffmpeg','-y','-v','error','-i',str(baseline),'-frames:v','1','-vf','scale=540:960',str(first)],log)
    tail_dir=work/'tail';tail_dir.mkdir(exist_ok=True)
    command(['ffmpeg','-y','-v','error','-ss',f'{(n-spec.frames)/spec.fps:.6f}',
             '-i',str(baseline),'-frames:v',str(spec.frames),'-vf','scale=540:960',str(tail_dir/'%03d.png')],log)
    paths=sorted(tail_dir.glob('*.png'))
    if len(paths)!=spec.frames:
        raise AssertionError(f'Tail count {len(paths)} != {spec.frames}')
    opening=np.asarray(Image.open(first).convert('RGB'))
    for i,p in enumerate(paths):
        old=np.asarray(Image.open(p).convert('RGB'))
        Image.fromarray(bridge_frame(old,opening,i,spec)).save(work/f'{i:03d}.png')
    segment=work/'segment.mp4'
    command(['ffmpeg','-y','-v','error','-framerate',str(spec.fps),'-i',str(work/'%03d.png'),
             '-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','ultrafast',
             '-crf','19','-pix_fmt','yuv420p','-an',str(segment)],log)
    head=n-spec.frames
    fc=f'[0:v]trim=end_frame={head},setpts=PTS-STARTPTS[h];[1:v]setpts=PTS-STARTPTS[t];[h][t]concat=n=2:v=1:a=0[v]'
    command(['ffmpeg','-y','-v','error','-i',str(baseline),'-i',str(segment),
             '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-c:a','copy',
             '-movflags','+faststart',str(output)],log)
    result=probe(output,log)
    outv=next(s for s in result['streams'] if s['codec_type']=='video')
    if int(outv['nb_frames'])!=n:
        raise AssertionError('Output frame count changed')
    return {'genre':spec.genre,'genre_label':GENRES[spec.genre], 'frames':n,
            'bridge_frames':spec.frames,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'narration':'ABSENT','spoken_caption_sync':'NOT_VERIFIED',
            'rights':'INHERITED_UNAPPROVED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--work',required=True,type=Path)
    ap.add_argument('--genre',default='ai_work',choices=GENRES)
    a=ap.parse_args()
    print(json.dumps(render(a.baseline,a.output,a.work,BridgeSpec(genre=a.genre)),ensure_ascii=False,indent=2))
