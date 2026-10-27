"""cycle907: original 3-act chapter rail + fail-closed Japanese ASR alignment QA.
Reimplementation for PRIVATE HUMAN REVIEW only, not original v33 code.
"""
from __future__ import annotations
import argparse
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work', 'business', 'education', 'finance', 'health', 'lifestyle',
          'technology', 'travel', 'food', 'entertainment')
ACTS = ('課題', '手順', '確認')
BOUNDARIES = (0., 5.667, 17., 23.033333)
RAIL_POS = (355, 28)
RAIL_SIZE = (360, 72)
CAPTION_START_Y = 1280
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('command failed: ' + repr(args[:7]) + '\n' + result.stderr[-2500:])
    return result.stdout

def validate_manifest(m):
    if m.get('genre') not in GENRES:
        raise ValueError('unknown genre')
    for key in ('publication_approved', 'employee_approval', 'asset_rights_approved',
                'upload_media_to_github', 'automatic_posting', 'paid_service',
                'independent_japanese_asr_verified', 'caption_semantics_verified'):
        if m.get(key) is not False:
            raise ValueError(key + ' must explicitly be false for review')
    digest = m.get('source_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ValueError('source SHA256 required')
    return True

def act_for_time(t):
    if not 0 <= t < BOUNDARIES[-1] + .001:
        raise ValueError('time outside video')
    return min(2, next((i for i in range(3) if t < BOUNDARIES[i + 1]), 2))

def japanese_font(size):
    for path in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
                 '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc'):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError('Japanese Noto font missing')

def rail_image(active):
    if active not in range(3):
        raise ValueError('invalid act')
    im = Image.new('RGBA', RAIL_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 359, 71), radius=19,
                        fill=(1, 17, 31, 237), outline=(45, 125, 149, 240), width=2)
    f = japanese_font(24)
    for i, word in enumerate(ACTS):
        x = 10 + i * 116
        is_active = active == i
        d.rounded_rectangle((x, 11, x + 108, 60), radius=13,
                            fill=(8, 137, 150, 255) if is_active else (12, 40, 58, 255),
                            outline=(98, 240, 223, 255) if is_active else (49, 94, 116, 255),
                            width=2 if is_active else 1)
        box = d.textbbox((0, 0), word, font=f)
        tw = box[2] - box[0]
        d.text((x + (108 - tw) / 2, 16), word, font=f,
               fill=(255, 255, 255, 255) if is_active else (158, 190, 205, 255))
    return im

def normalize_ja(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s).lower()
                   if unicodedata.category(c)[0] not in ('P', 'Z', 'C'))

def audit_transcript(cues, independent_asr, tolerance=.45, threshold=.86):
    """Compare independent ASR to caption cues. This function DOES NOT run ASR."""
    if not independent_asr:
        return {'passed': False, 'reason': 'INDEPENDENT_JAPANESE_ASR_MISSING', 'checked': 0}
    if not cues:
        return {'passed': False, 'reason': 'CAPTION_CUES_MISSING', 'checked': 0}
    if len(cues) != len(independent_asr):
        return {'passed': False, 'reason': 'SEGMENT_COUNT_MISMATCH', 'checked': 0}
    checks = []
    for cue, spoken in zip(cues, independent_asr):
        if any(k not in row for row in (cue, spoken) for k in ('start', 'end', 'text')):
            return {'passed': False, 'reason': 'INVALID_SEGMENT', 'checked': len(checks)}
        if not (0 <= cue['start'] < cue['end'] and 0 <= spoken['start'] < spoken['end']):
            return {'passed': False, 'reason': 'INVALID_TIMING', 'checked': len(checks)}
        a, b = normalize_ja(cue['text']), normalize_ja(spoken['text'])
        score = SequenceMatcher(None, a, b).ratio() if a and b else 0.
        drift = max(abs(cue['start'] - spoken['start']), abs(cue['end'] - spoken['end']))
        checks.append({'similarity': round(score, 3), 'drift_seconds': round(drift, 3),
                       'passed': score >= threshold and drift <= tolerance})
    passed = all(c['passed'] for c in checks)
    return {'passed': passed, 'checked': len(checks),
            'reason': 'PASS' if passed else 'SEMANTIC_OR_TIMING_MISMATCH', 'segments': checks}

def probe(path):
    obj = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                          '-of', 'json', str(path)]))
    v = next(s for s in obj['streams'] if s['codec_type'] == 'video')
    a = next(s for s in obj['streams'] if s['codec_type'] == 'audio')
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate'], int(v['nb_frames'])) != ('h264', 1080, 1920, '30/1', 691):
        raise ValueError('unexpected video format')
    if (a['codec_name'], a['sample_rate']) != ('aac', '48000'):
        raise ValueError('unexpected audio format')
    return {'video': 'h264', 'audio': 'aac', 'size': [1080, 1920], 'fps': 30,
            'frames': 691, 'duration': float(obj['format']['duration'])}

def aac_sha(path, work):
    dest = Path(work) / (Path(path).stem + '.aac')
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vn', '-c:a', 'copy', '-f', 'adts', str(dest)])
    return sha256(dest)

def render(source, output, manifest, work):
    source, output, work = Path(source).resolve(), Path(output).resolve(), Path(work).resolve()
    m = json.loads(Path(manifest).read_text(encoding='utf-8'))
    validate_manifest(m)
    if output.exists() or output == source:
        raise ValueError('output already exists; no overwrite')
    if sha256(source) != m['source_sha256']:
        raise ValueError('source SHA mismatch')
    probe(source)
    if RAIL_POS[1] + RAIL_SIZE[1] >= CAPTION_START_Y:
        raise AssertionError('subtitle area collision')
    work.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(3):
        p = work / f'act_{i}.png'
        rail_image(i).save(p)
        paths.append(p)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source)]
    for p in paths:
        cmd += ['-loop', '1', '-framerate', '30', '-i', str(p)]
    filters = ("[0:v][1:v]overlay=355:28:enable='lt(t,5.667)':shortest=1[v1];"
               "[v1][2:v]overlay=355:28:enable='between(t,5.667,16.999)':shortest=1[v2];"
               "[v2][3:v]overlay=355:28:enable='gte(t,17)':shortest=1[v]")
    cmd += ['-filter_complex', filters, '-map', '[v]', '-map', '0:a:0',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
            '-c:a', 'copy', '-frames:v', '691', '-movflags', '+faststart', str(output)]
    run(cmd)
    result = probe(output)
    run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'])
    audio_same = aac_sha(source, work) == aac_sha(output, work)
    if not audio_same:
        raise AssertionError('AAC bitstream changed')
    return {'status': STATUS, 'source_sha256': sha256(source), 'output_sha256': sha256(output),
            'audio_bitstream_identical': audio_same, 'full_av_decode': True,
            'acts': list(ACTS), 'boundaries': list(BOUNDARIES),
            'subtitle_area_untouched_by_overlay': True,
            'independent_japanese_asr': 'NOT_AVAILABLE',
            'caption_semantic_timing': audit_transcript([], []),
            'asset_rights_approved': False, 'employee_approval': False,
            'publication_allowed': False, **result}

def publication_gate(_):
    raise PermissionError('PUBLICATION_NOT_APPROVED: ASR, rights, human approval and device test missing')

def main():
    p = argparse.ArgumentParser()
    for key in ('source', 'output', 'manifest', 'work', 'report'):
        p.add_argument('--' + key, required=True)
    a = p.parse_args()
    result = render(a.source, a.output, a.manifest, a.work)
    Path(a.report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
