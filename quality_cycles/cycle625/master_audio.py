#!/usr/bin/env python3
"""Zero-cost, rights-conservative audio headroom for vertical slide videos.

Keep H.264 bitstream *exactly* unchanged, apply a gentle transparent peak
limiter to inherited Japanese narration/SFX, and re-encode AAC. This does NOT
validate Japanese pronunciation, transcription, rights or publishing approval.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PROFILES = HERE / 'audio_profiles.json'


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)]))


def load_profile(config: Path, genre: str) -> dict:
    obj = json.loads(config.read_text(encoding='utf-8'))
    if obj.get('publication') != 'NOT_APPROVED' or len(obj.get('genres', {})) != 10:
        raise ValueError('Expected 10 genres and NOT_APPROVED publication')
    if genre not in obj['genres']:
        raise ValueError(f'Unknown genre: {genre}')
    p = obj['genres'][genre]
    limit, attack, release, gain = (float(p[k]) for k in
        ('limiter_limit', 'attack_ms', 'release_ms', 'gain_db'))
    if not (.5 <= limit <= .95 and 1 <= attack <= 20 and 20 <= release <= 250
            and -3 <= gain <= 0):
        raise ValueError('Unsafe profile: limiter/gain outside conservative bounds')
    return p


def audio_filter(profile: dict) -> str:
    return ('alimiter=limit={limiter_limit}:attack={attack_ms}:release={release_ms}:'
            'level=0:latency=1,volume={gain_db}dB').format(**profile)


def render(source: Path, output: Path, config: Path, genre: str) -> dict:
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError('Source and output must differ')
    profile = load_profile(config, genre)
    streams = probe(source)['streams']
    v = next((s for s in streams if s['codec_type'] == 'video'), None)
    a = next((s for s in streams if s['codec_type'] == 'audio'), None)
    if v is None or a is None or (v['codec_name'], v['width'], v['height']) != ('h264',1080,1920):
        raise ValueError('Requires existing 1080x1920 H.264 video with audio')
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
           '-map','0:v:0','-map','0:a:0','-c:v','copy',
           '-af',audio_filter(profile),'-c:a','aac','-b:a','192k',
           '-ar','48000','-ac','2','-movflags','+faststart',
           '-metadata','comment=HUMAN_REVIEW_PUBLICATION_NOT_APPROVED',str(output)]
    run(cmd)
    return {'source':str(source),'output':str(output),'genre':genre,
            'profiles':10,'audio_filter':audio_filter(profile),
            'video':'BITSTREAM_COPY','publication':'NOT_APPROVED','status':'HUMAN_REVIEW'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--config',type=Path,default=DEFAULT_PROFILES)
    p.add_argument('--genre',default='雑学・科学')
    args = p.parse_args()
    print(json.dumps(render(args.input,args.output,args.config,args.genre),ensure_ascii=False,indent=2))
