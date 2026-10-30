#!/usr/bin/env python3
"""Review-only two-beat evidence focus on inherited spreadsheet UI.

Never uploads or publishes source footage. This is a visual pointer, NOT proof
of independent Japanese speech/subtitle alignment or source-asset rights.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': ('営業A', '営業B', '46', '29'),
    'beauty': ('比較A', '比較B', '確認', '確認'),
    'romance_psychology': ('視点A', '視点B', '確認', '確認'),
    'money_saving': ('支出A', '支出B', '確認', '確認'),
    'sales_business': ('集計A', '集計B', '確認', '確認'),
    'career': ('条件A', '条件B', '確認', '確認'),
    'health_lifestyle': ('記録A', '記録B', '確認', '確認'),
    'science_trivia': ('仮説A', '仮説B', '確認', '確認'),
    'travel_food': ('候補A', '候補B', '確認', '確認'),
    'product_comparison_lifestyle': ('商品A', '商品B', '確認', '確認'),
}

def run(args, binary=False):
    p = subprocess.run([str(x) for x in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return p.stdout if binary else p.stdout.decode('utf-8')

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]))

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0', '-c', 'copy', '-f', 'adts', '-'], True)).hexdigest()

def safe_text(s):
    if any(c in s for c in "\\:'%,\n"):
        raise ValueError('unsafe overlay text')
    return s

def filter_graph(genre, start=5.95, middle=7.20, end=8.55):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 0 <= start < middle < end:
        raise ValueError('invalid intervals')
    a, b, av, bv = GENRES[genre]
    filters = []
    for i, (label, value, x, color, t0, t1) in enumerate((
        (a, av, 44, '0x36e2c7', start, middle),
        (b, bv, 548, '0x73c8ff', middle, end),
    ), 1):
        enable = f'between(t,{t0:.3f},{t1:.3f})'
        filters += [
            f"drawbox=x=74:y=317:w=832:h=95:color=0x092538@0.92:t=fill:enable='{enable}'",
            f"drawbox=x=74:y=317:w=11:h=95:color={color}@1:t=fill:enable='{enable}'",
            f"drawtext=fontfile={FONT}:text='{safe_text(str(i).zfill(2) + '  ' + label + '  ' + value + ' を確認')}':fontsize=47:fontcolor=white:x=105:y=331:enable='{enable}'",
            f"drawbox=x={x}:y=1154:w=480:h=144:color={color}@0.96:t=8:enable='{enable}'",
            f"drawbox=x={x+12}:y=1303:w=456:h=8:color={color}@0.90:t=fill:enable='{enable}'",
        ]
    return ','.join(filters)

def render(source, output, report, genre, expected_sha, review_only=False, synthetic_ci=False):
    if not review_only:
        raise ValueError('human review gate required')
    source, output, report = (Path(p).resolve() for p in (source, output, report))
    if not source.is_file() or source == output or output.exists() or report.exists():
        raise ValueError('missing source or existing output')
    if len(expected_sha) != 64 or sha(source) != expected_sha:
        raise ValueError('source SHA mismatch')
    info = probe(source)
    video = [s for s in info['streams'] if s['codec_type'] == 'video']
    audio = [s for s in info['streams'] if s['codec_type'] == 'audio']
    if len(info['streams']) != 2 or len(video) != 1 or len(audio) != 1:
        raise ValueError('exactly one video and one audio stream required')
    v, a = video[0], audio[0]
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate'], a['codec_name'], int(a['sample_rate'])) != ('h264', 1080, 1920, '30/1', 'aac', 48000):
        raise ValueError('invalid media specification')
    start, middle, end = (0.10, 0.88, 1.85) if synthetic_ci else (5.95, 7.20, 8.55)
    if float(info['format']['duration']) < end - 0.02:
        raise ValueError('source too short')
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y', '-i', source,
         '-map', '0:v:0', '-map', '0:a:0', '-vf', filter_graph(genre, start, middle, end),
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-threads', '2',
         '-c:a', 'copy', '-metadata:s:a:0', 'language=jpn', '-movflags', '+faststart', output])
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', output, '-f', 'null', '-'])
    after = probe(output)
    vv = next(s for s in after['streams'] if s['codec_type'] == 'video')
    if (vv['width'], vv['height'], vv['r_frame_rate']) != (1080, 1920, '30/1'):
        raise RuntimeError('video format changed')
    unchanged = audio_sha(source) == audio_sha(output)
    if not unchanged:
        raise RuntimeError('audio payload changed')
    result = {'source_sha256': sha(source), 'output_sha256': sha(output), 'genre': genre,
              'duration_seconds': float(after['format']['duration']), 'frames': int(vv.get('nb_frames', 0)),
              'video': 'H.264 1080x1920 30fps', 'audio': 'AAC 48kHz Japanese-tagged',
              'audio_bitstream_unchanged': unchanged, 'full_av_decode': 'PASS',
              'change': 'scene03 sequential focus on spreadsheet A/B result cards',
              'change_window_seconds': [start, end], 'subtitle_safe_y_min': 1490,
              'independent_japanese_asr': 'NOT_PERFORMED', 'caption_semantic_sync': 'NOT_VERIFIED',
              'source_rights': 'NOT_VERIFIED', 'employee_approval': 'NOT_APPROVED',
              'publication': 'NOT_APPROVED'}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--genre', choices=sorted(GENRES), default='ai_work')
    parser.add_argument('--expected-source-sha', required=True)
    parser.add_argument('--review-only', action='store_true')
    parser.add_argument('--synthetic-ci', action='store_true')
    args = parser.parse_args()
    print(json.dumps(render(args.source, args.output, args.report, args.genre, args.expected_source_sha, args.review_only, args.synthetic_ci), ensure_ascii=False))
