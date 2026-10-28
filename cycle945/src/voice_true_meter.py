"""Review-only audio-reactive waveform. No ASR, no uploads, no posting.

Replaces the old decorative waveform in the existing caption-safe strip with a
measured amplitude trace. The measured signal includes ambient sound and is NOT
proof that spoken Japanese matches burned subtitles.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

GENRES = ('ai_work','business','finance','health','education','lifestyle','technology','career','productivity','travel')
PALETTES = {
    'ai_work': (61,218,214), 'business': (93,179,234), 'finance': (107,220,178),
    'health': (114,214,178), 'education': (244,185,99), 'lifestyle': (222,151,215),
    'technology': (115,174,248), 'career': (243,176,111),
    'productivity': (107,212,209), 'travel': (126,205,238),
}
FPS = 30
SAMPLE_RATE = 16000
OVERLAY_X, OVERLAY_Y = 89, 1707
OVERLAY_W, OVERLAY_H = 440, 66
TEXT_SAFE_END_Y = 1698
PROGRESS_SAFE_START_Y = 1780


def read_mono_audio(path: Path) -> np.ndarray:
    p = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(SAMPLE_RATE),'-f','f32le','-'],capture_output=True,check=True)
    return np.frombuffer(p.stdout,dtype='<f4').copy()


def frame_levels(audio: np.ndarray, frame_count: int, fps: int = FPS, sr: int = SAMPLE_RATE) -> np.ndarray:
    """RMS energy in the 40ms ending at each video frame; no speech inference."""
    if frame_count < 1 or fps <= 0 or sr <= 0: raise ValueError('invalid timebase')
    if audio.ndim != 1: raise ValueError('mono audio required')
    if not np.isfinite(audio).all(): raise ValueError('nonfinite audio')
    result = np.empty(frame_count,dtype=np.float32)
    span = max(1,round(sr*.040))
    for i in range(frame_count):
        end = min(len(audio),round((i+1)*sr/fps))
        start = max(0,end-span)
        a = audio[start:end]
        result[i] = float(np.sqrt(np.mean(a.astype(np.float64)**2))) if len(a) else 0
    return result


def level_to_height(level: float, max_h: int = 39) -> int:
    """Decibel-compressed amplitude, safe even for digital silence."""
    if not math.isfinite(level) or level < 0: raise ValueError('invalid level')
    db = 20*math.log10(max(level,1e-8))
    return max(3,min(max_h,round(3+(max_h-3)*np.clip((db+47)/35,0,1))))


def meter_image(levels: np.ndarray, frame_index: int, genre: str = 'ai_work') -> Image.Image:
    if genre not in GENRES: raise ValueError('unknown genre')
    if not 0 <= frame_index < len(levels): raise IndexError(frame_index)
    # Full-opacity backing deliberately covers only the pre-existing ornamental bars.
    im = Image.new('RGBA',(OVERLAY_W,OVERLAY_H),(3,11,26,255))
    d = ImageDraw.Draw(im)
    color = PALETTES[genre]
    # 24 bars: last 0.8 seconds, one sample each frame. Rightmost = current frame.
    x0, gap, bar_w, n = 13, 17, 8, 24
    for j in range(n):
        k = max(0,frame_index-(n-1-j))
        h = level_to_height(float(levels[k]))
        x = x0+j*gap
        y = 50-h
        # Reduce edge shimmer, but keep amplitude true; no arbitrary random heights.
        d.rounded_rectangle((x,y,x+bar_w,50),radius=3,fill=(*color,235))
    d.line((13,57,408,57),fill=(*color,55),width=1)
    return im


def probe_video(path: Path) -> tuple[int,int,int,float]:
    p = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,nb_read_frames,r_frame_rate','-of','json',str(path)],capture_output=True,text=True,check=True)
    st=json.loads(p.stdout)['streams'][0]
    n=int(st['nb_read_frames'])
    rate=st['r_frame_rate'].split('/')
    fps=float(rate[0])/float(rate[1])
    return int(st['width']),int(st['height']),n,fps


def render(source: Path, output: Path, genre: str = 'ai_work') -> dict:
    source=Path(source);output=Path(output)
    if genre not in GENRES: raise ValueError('unknown genre')
    if not source.is_file(): raise FileNotFoundError(source)
    w,h,n,fps=probe_video(source)
    if (w,h)!=(1080,1920) or abs(fps-FPS)>.001: raise ValueError('unexpected input dimensions/fps')
    if OVERLAY_Y <= TEXT_SAFE_END_Y or OVERLAY_Y+OVERLAY_H >= PROGRESS_SAFE_START_Y:
        raise AssertionError('caption/progress safe bounds violated')
    levels=frame_levels(read_mono_audio(source),n)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
         '-f','rawvideo','-pixel_format','rgba','-video_size',f'{OVERLAY_W}x{OVERLAY_H}',
         '-framerate',str(FPS),'-i','pipe:0',
         '-filter_complex',f'[0:v][1:v]overlay={OVERLAY_X}:{OVERLAY_Y}:shortest=1:format=auto,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(n),'-c:a','copy',
         '-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(n):
            p.stdin.write(meter_image(levels,i,genre).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        ret=p.wait()
        if ret: raise RuntimeError(f'ffmpeg failed ({ret}): {err[-1500:]}')
    except Exception:
        if p.poll() is None: p.kill()
        output.unlink(missing_ok=True)
        raise
    return {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'frames':n,'fps':fps,'genre':genre,'energy_max':float(levels.max()),
            'energy_min':float(levels.min()),'replaced_area':[OVERLAY_X,OVERLAY_Y,OVERLAY_W,OVERLAY_H],
            'scope':'audio amplitude proxy only; NOT speech recognition or subtitle semantics',
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--source',type=Path,required=True)
    a.add_argument('--output',type=Path,required=True)
    a.add_argument('--genre',choices=GENRES,default='ai_work')
    args=a.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
