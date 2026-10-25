"""Cycle840: keep cycle838 dissolves while applying cycle839 shared A/V pacing.

Fail-closed, local-only and HUMAN_REVIEW. Never publishes or uploads media.
This is a reimplementation, not the original v33 generator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from cycle839 import pacing
from cycle833.focal_layout import GENRES as LAYOUT_GENRES

# The older layout calls its tenth genre "productivity", while the newer EDL
# calls it "product_comparison_lifestyle". Map explicitly, never silently drop it.
PACING_ALIASES = {"productivity": "product_comparison_lifestyle"}
CANONICAL_GENRES = tuple(LAYOUT_GENRES)

REQUIRED = {
    'data_classification': 'fictional',
    'contains_personal_data': False,
    'review_only': True,
    'publication_approved': False,
    'source_rights_reviewed': False,
    'external_upload': False,
    'automatic_posting': False,
    'contains_cycle838_dissolves': True,
}

def validate_manifest(manifest: dict, genre: str) -> None:
    if (genre not in CANONICAL_GENRES or len(CANONICAL_GENRES) != 10
            or set(PACING_ALIASES.get(g,g) for g in CANONICAL_GENRES) != set(pacing.GENRES)):
        raise ValueError('Unknown genre or missing 10-genre configuration')
    if not isinstance(manifest, dict) or any(manifest.get(k) != v for k, v in REQUIRED.items()):
        raise ValueError('Only fictional, local, unapproved review source with cycle838 dissolves is permitted')
    if not isinstance(manifest.get('source_sha256'), str) or len(manifest['source_sha256']) != 64:
        raise ValueError('Pinned source_sha256 required')

def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format',
                                               '-of','json',str(path)], text=True))

def av_metrics(meta: dict) -> tuple[dict, dict, float]:
    streams = meta.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    if not video or not audio:
        raise ValueError('Missing video or audio stream')
    if video.get('codec_name') != 'h264' or video.get('width') != 1080 or video.get('height') != 1920:
        raise ValueError('Unexpected video format or resolution')
    if audio.get('codec_name') != 'aac' or audio.get('sample_rate') != '48000':
        raise ValueError('Unexpected audio codec or sample rate')
    if video.get('r_frame_rate') != '30/1':
        raise ValueError('Expected 30 fps')
    return video, audio, float(meta['format']['duration'])

def assert_av(path: Path, expected_frames: int) -> dict:
    v, a, duration = av_metrics(probe(path))
    expected_duration = expected_frames / pacing.FPS
    audio_duration = float(a.get('duration', 0))
    if int(v.get('nb_frames', -1)) != expected_frames:
        raise ValueError('Frame count mismatch')
    if abs(duration - expected_duration) > 0.06:
        raise ValueError('Video duration mismatch')
    if audio_duration < expected_duration - 0.15 or audio_duration > expected_duration + 0.15:
        raise ValueError(f'Audio incomplete: {audio_duration:.3f}s vs {expected_duration:.3f}s video')
    return {'video_seconds': duration, 'audio_seconds': audio_duration, 'frames': expected_frames}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def run(source: Path, output: Path, manifest: dict, genre: str='ai_work') -> dict:
    validate_manifest(manifest, genre)
    source, output = Path(source), Path(output)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('Source missing or output would overwrite source')
    if sha256(source) != manifest['source_sha256']:
        raise ValueError('Source SHA-256 mismatch')
    old = assert_av(source, 775)  # Catches the prior 0.704-second audio failure.
    result = pacing.render(source, source, output, genre=PACING_ALIASES.get(genre, genre))
    new = assert_av(output, 691)
    # Independent full decode, not merely codec metadata.
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True, timeout=180)
    gaps = pacing.silences(output, minimum=0.02)
    # Estimated audible activity at -35 dB, NOT a verified Japanese transcript.
    estimated_non_silent_seconds = new['audio_seconds'] - sum(max(0.,b-a) for a,b in gaps)
    if estimated_non_silent_seconds < 14:
        raise ValueError('Output has insufficient audible content')
    return {'genre':genre,'pacing_genre':PACING_ALIASES.get(genre, genre),'source_sha256':manifest['source_sha256'],
            'output_sha256':sha256(output),'source':old,'output':new,
            'removed_seconds':result['removed_seconds'],'cuts':result['cuts'],
            'estimated_non_silent_seconds_at_minus35db':round(estimated_non_silent_seconds,3),
            'dissolves_retained_from_source':True,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'speech_semantic_verified':False,'phone_verified':False,
            'rights_approved':False,'reference_v33_compared':False}

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--genre',default='ai_work')
    a=ap.parse_args()
    print(json.dumps(run(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))
