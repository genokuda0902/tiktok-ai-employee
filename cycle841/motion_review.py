"""Cycle841: local-only, audio-preserving subtle motion on static image scenes.

Reimplementation; never publishes or uploads private media. Ten-genre shared
motion filter, restricted to image area; title, CTA and burned captions stay put.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'productivity')
FPS = 30
SCENE_FRAMES = (89, 81, 79, 87, 86, 89, 77, 103)  # cycle840 after 7 trims
TARGET_SCENES = (1, 5, 7)  # 0-based: static scenes only, not live PC footage
REGION = (45, 370, 960, 760)  # only visual inset, never title or burned subtitles
REQUIRED = {'data_classification': 'fictional', 'contains_personal_data': False,
            'review_only': True, 'publication_approved': False,
            'external_upload': False, 'automatic_posting': False,
            'source_rights_reviewed': False}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def validate_manifest(manifest: dict, genre: str) -> None:
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('Unknown genre or incomplete ten-genre configuration')
    if not isinstance(manifest, dict) or any(manifest.get(k) != v for k, v in REQUIRED.items()):
        raise ValueError('Only fictional, local, unapproved review media allowed')
    if not isinstance(manifest.get('source_sha256'), str) or len(manifest['source_sha256']) != 64:
        raise ValueError('Source SHA256 pin is mandatory')
    if manifest.get('contains_confidential_media') is not False:
        raise ValueError('Explicit no-confidential-media confirmation required')


def ranges():
    bounds = [0]
    for n in SCENE_FRAMES:
        bounds.append(bounds[-1] + n)
    return [(bounds[i], bounds[i+1]) for i in TARGET_SCENES]


def filtergraph():
    # Smooth ease in/out: the zoom returns to 1.0 at both scene boundaries,
    # protecting existing seven scene dissolves. Outside three whitelisted
    # scenes, original pixels pass through unmodified before H264 encoding.
    terms = [f'0.044*max(0,sin(PI*(on-{a})/{b-a}))*between(on,{a},{b-1})'
             for a, b in ranges()]
    zoom = '1+' + '+'.join(terms)
    enable = '+'.join(f'between(n,{a},{b-1})' for a, b in ranges())
    x, y, w, h = REGION
    return (f'[0:v]split=2[base][raw];'
            f'[raw]crop={w}:{h}:{x}:{y},'
            f"zoompan=z='{zoom}':x='(iw-iw/zoom)/2+3*sin(on/17)':"
            f"y='(ih-ih/zoom)/2+2*cos(on/23)':d=1:s={w}x{h}:fps={FPS},"
            f'format=yuv420p[focus];'
            f"[base][focus]overlay={x}:{y}:enable='{enable}':shortest=1:format=auto[v]")


def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-show_streams','-show_format','-of','json',str(path)],text=True))


def verify_av(path: Path) -> dict:
    p = probe(path)
    v = next((s for s in p['streams'] if s.get('codec_type') == 'video'), None)
    a = next((s for s in p['streams'] if s.get('codec_type') == 'audio'), None)
    if not v or not a or v.get('codec_name') != 'h264' or a.get('codec_name') != 'aac':
        raise ValueError('H264 video and AAC audio both required')
    if (v.get('width'),v.get('height'),v.get('r_frame_rate')) != (1080,1920,'30/1'):
        raise ValueError('Unexpected image size or frame rate')
    if int(v.get('nb_frames', -1)) != sum(SCENE_FRAMES):
        raise ValueError('Unexpected frame count')
    if abs(float(a.get('duration', 0))-sum(SCENE_FRAMES)/FPS) > .15:
        raise ValueError('Truncated audio')
    return {'frames': int(v['nb_frames']), 'video_seconds':float(v['duration']),
            'audio_seconds':float(a['duration']), 'width':v['width'], 'height':v['height']}


def audio_pcm_md5(path: Path) -> str:
    # Independently compares decoded audio, rather than only file container bytes.
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
        '-map','0:a:0','-f','s16le','-acodec','pcm_s16le','-ar','48000','-ac','2','-'])
    return hashlib.md5(raw).hexdigest()


def render(source: Path, output: Path, manifest: dict, genre='ai_work') -> dict:
    validate_manifest(manifest, genre)
    source, output = Path(source), Path(output)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('Source missing or output would overwrite input')
    if sha256(source) != manifest['source_sha256']:
        raise ValueError('Source SHA256 mismatch')
    before = verify_av(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2',
           '-filter_complex_threads','2','-i',str(source),'-filter_complex',filtergraph(),
           '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
           '-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    after = verify_av(output)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True,timeout=150)
    a0,a1=audio_pcm_md5(source),audio_pcm_md5(output)
    if a0 != a1:
        raise ValueError('Decoded narration audio changed')
    return {'genre':genre,'source_sha256':manifest['source_sha256'],
            'output_sha256':sha256(output),'source':before,'output':after,
            'motion_scene_indices_zero_based':list(TARGET_SCENES),
            'motion_ranges_frames':ranges(),'audio_pcm_md5_identical':True,
            'audio_pcm_md5':a1,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'speech_semantics_verified':False,'word_sync_verified':False,
            'rights_approved':False,'reference_v33_compared':False,'phone_verified':False}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))
