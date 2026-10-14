#!/usr/bin/env python3
"""cycle579: repair misleading reversed number animation at loop seam.

Review-only reimplementation. Requires exact reviewed source SHA. Does not
approve inherited assets, narration, or publication. No network or paid APIs.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ('ai_productivity', 'beauty', 'relationships', 'finance', 'sales',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison')
SOURCE_SHA256 = 'c0bb03263495f4b3bacbe1cf9e7f65c4187f4dce336aac70cc0713484f3f3cd7'
EXPECTED_TOTAL = 720
VALUES = (120, 150, 200, 250)
FREEZE_FRAME = 27  # 0.9s: 720 has completed its count-up.
FPS = 30


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def validate(genre, values=VALUES, total=EXPECTED_TOTAL, freeze_frame=FREEZE_FRAME):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    if len(values) != 4 or any(not isinstance(x, int) or x < 0 for x in values):
        raise ValueError('invalid proof values')
    if sum(values) != total:
        raise ValueError('misleading result: total mismatch')
    if not (24 <= freeze_frame <= 29):
        raise ValueError('freeze must use stable final proof frame')
    return True


def filter_graph():
    # 30 frozen frames at each boundary, 540 untouched middle frames.
    # 18-19s CTA preserved; 19-20s reversed numeric tween replaced.
    return ('[1:v]trim=duration=1,setpts=PTS-STARTPTS,split=2[head][tail];'
            '[0:v]trim=start_frame=30:end_frame=570,setpts=PTS-STARTPTS[center];'
            '[head][center][tail]concat=n=3:v=1:a=0,format=yuv420p[v];'
            '[0:a:0]afade=t=in:st=0:d=0.12,afade=t=out:st=19.88:d=0.12[a]')


def render(source, output, genre='ai_productivity'):
    validate(genre)
    if genre != 'ai_productivity':
        raise ValueError('no inspected input video for this genre')
    source, output = Path(source), Path(output)
    if not source.is_file() or sha256(source) != SOURCE_SHA256:
        raise ValueError('source missing or checksum mismatch')
    output.parent.mkdir(parents=True, exist_ok=True)
    still = output.parent / 'verified_720_frame.png'
    extract = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                              '-i', str(source), '-vf', f'select=eq(n\\,{FREEZE_FRAME})',
                              '-vsync', '0', '-frames:v', '1', str(still)],
                             capture_output=True, text=True)
    if extract.returncode or not still.is_file():
        raise RuntimeError('verified frame extraction failed: ' + extract.stderr[-1000:])
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-i', str(source), '-loop', '1', '-framerate', '30', '-i', str(still),
           '-filter_complex', filter_graph(),
           '-map', '[v]', '-map', '[a]', '-map', '0:s:0?',
           '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '19',
           '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k',
           '-c:s', 'mov_text', '-t', '20', '-movflags', '+faststart', str(output)]
    p = subprocess.run(cmd, text=True, capture_output=True)
    (output.parent / 'render.log').write_text(' '.join(cmd) + '\nreturncode=' + str(p.returncode) + '\n' + p.stderr)
    if p.returncode:
        raise RuntimeError(p.stderr[-3000:])
    report = {'cycle': 579, 'source_sha256': SOURCE_SHA256,
              'output_sha256': sha256(output), 'genre': genre,
              'proof_values': VALUES, 'verified_total': EXPECTED_TOTAL,
              'changed_windows_sec': [[0, 1], [19, 20]],
              'quality_change': 'constant verified 720 in opening and loop tail; audio edge fade',
              'japanese_narration': 'ABSENT', 'caption_speech_sync': 'UNVERIFIED',
              'asset_rights': 'INHERITED_UNVERIFIED',
              'quality': 'HUMAN_REVIEW', 'publication': 'NOT_APPROVED', 'cost_jpy': 0}
    (output.parent / 'qa.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', default='ai_productivity')
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output, a.genre), ensure_ascii=False, indent=2))
