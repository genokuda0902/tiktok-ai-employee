"""Selective illustration clarity lift for review-only Japanese slide MP4s.

Improves dim midtone graphics in y=370..1220 while preserving titles and
Japanese subtitle card. No text generation, transcription or publishing.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

WIDTH, HEIGHT, FPS = 1080, 1920, 30
Y_TOP, Y_BOTTOM, FEATHER = 370, 1220, 52
GENRES = ('ai_workflow', 'business', 'finance', 'health', 'beauty',
          'travel', 'education', 'lifestyle', 'technology', 'entertainment')
PRESETS = {g: {'gamma': 1.12, 'contrast': 1.035, 'saturation': 1.065,
               'brightness': 0.008} for g in GENRES}

def alpha_at(y: int, top: int = Y_TOP, bottom: int = Y_BOTTOM,
             feather: int = FEATHER) -> int:
    if not (0 <= top < bottom <= HEIGHT and 0 < feather * 2 < bottom-top):
        raise ValueError('Invalid enhancement bounds')
    if y < top or y >= bottom:
        return 0
    return round(255 * min(1., (y-top)/feather, (bottom-1-y)/feather))

def make_mask(path: str | Path, width: int = WIDTH, height: int = HEIGHT,
              top: int = Y_TOP, bottom: int = Y_BOTTOM,
              feather: int = FEATHER) -> Path:
    if not (0 <= top < bottom <= height and 0 < feather * 2 < bottom-top):
        raise ValueError('Invalid bounds')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new('L', (width, bottom-top))
    for i in range(bottom-top):
        a = alpha_at(i+top, top, bottom, feather)
        image.paste(a, (0, i, width, i+1))
    image.save(path)
    return path

def probe(path: str | Path) -> dict:
    raw = json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-show_streams','-show_format','-of','json',str(path)], text=True))
    video = next(s for s in raw['streams'] if s['codec_type']=='video')
    audio = next(s for s in raw['streams'] if s['codec_type']=='audio')
    return {'width': int(video['width']), 'height': int(video['height']),
        'fps': video['avg_frame_rate'], 'frames': int(video.get('nb_frames',0)),
        'duration': float(raw['format']['duration']), 'video_codec': video['codec_name'],
        'audio_codec': audio['codec_name'], 'sample_rate': int(audio['sample_rate']),
        'language': audio.get('tags',{}).get('language','und')}

def validate_source(info: dict) -> None:
    if (info['width'],info['height'],info['fps']) != (WIDTH,HEIGHT,'30/1'):
        raise ValueError('Source must be 1080x1920 at 30 fps')
    if info['audio_codec']!='aac' or info['sample_rate']!=48000:
        raise ValueError('Source must have AAC 48kHz')

def filter_graph(preset: dict = None) -> str:
    p = preset or PRESETS['ai_workflow']
    h = Y_BOTTOM-Y_TOP
    return (f'[0:v]split[base][copy];'
            f'[copy]crop={WIDTH}:{h}:0:{Y_TOP},'
            f'eq=gamma={p["gamma"]}:contrast={p["contrast"]}:'
            f'saturation={p["saturation"]}:brightness={p["brightness"]},'
            f'format=rgb24[graded];'
            f'[1:v]format=gray[mask];'
            f'[graded][mask]alphamerge[overlay];'
            f'[base][overlay]overlay=0:{Y_TOP}:format=auto:shortest=1,'
            'format=yuv420p[v]')

def render(source: str | Path, target: str | Path, genre: str = 'ai_workflow',
           max_frames: int | None = None) -> dict:
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    source, target = Path(source), Path(target)
    if not source.is_file():
        raise FileNotFoundError(source)
    info = probe(source)
    validate_source(info)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='illustration_lift_') as d:
        mask = make_mask(Path(d)/'feather.png')
        cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
               '-i',str(source),'-loop','1','-framerate',str(FPS),'-i',str(mask),
               '-filter_complex',filter_graph(PRESETS[genre]),
               '-map','[v]','-map','0:a:0','-c:v','libx264',
               '-preset','veryfast','-crf','20','-threads','4',
               '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
               '-map_metadata','0','-map_chapters','0','-movflags','+faststart']
        if max_frames is not None:
            if max_frames < 1: raise ValueError('max_frames must be positive')
            cmd += ['-frames:v',str(max_frames)]
        cmd.append(str(target))
        subprocess.run(cmd, check=True)
    return {'genre': genre, 'source': str(source), 'target': str(target),
            'enhancement_y': [Y_TOP,Y_BOTTOM], 'feather_px': FEATHER,
            'settings': PRESETS[genre], 'source_audio_stream_copy': True,
            'independent_japanese_asr': 'NOT VERIFIED',
            'publication_status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source'); parser.add_argument('target')
    parser.add_argument('--genre', choices=GENRES, default='ai_workflow')
    parser.add_argument('--max-frames', type=int)
    a=parser.parse_args()
    print(json.dumps(render(a.source,a.target,a.genre,a.max_frames),ensure_ascii=False,indent=2))
