#!/usr/bin/env python3
"""Offline chapter focus cue for vertical Japanese narrated slides.

Never posts, merges, uploads media, or accesses a paid service. The caller must
supply a reviewed target rectangle; no automatic inference of private content.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PALETTES = {
    'ai': '#54E8D5', 'business': '#73B9FF', 'money': '#E7CB72',
    'learning': '#9AC5FF', 'health': '#72D4B3', 'food': '#FFB783',
    'travel': '#83D9EA', 'beauty': '#F0A9CF', 'career': '#AFB4FF',
    'life': '#A8D9A1',
}
W, H, FPS = 1080, 1920, 30


def run(cmd):
    p = subprocess.run([str(x) for x in cmd], capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-1800:])
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_chapters', '-show_format', '-of', 'json', path]))


def streams(meta):
    return (next(s for s in meta['streams'] if s['codec_type'] == 'video'),
            next(s for s in meta['streams'] if s['codec_type'] == 'audio'))


def aac_hash(path):
    raw = run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0',
               '-c:a', 'copy', '-f', 'adts', 'pipe:1'])
    return hashlib.sha256(raw).hexdigest()


def validate_rect(rect):
    x, y, w, h = map(int, rect)
    if w < 60 or h < 40 or x < 32 or y < 360 or x + w > W - 32 or y + h > 1340:
        raise ValueError('Focus cue must remain in central visual panel, not subtitle/footer')
    return x, y, w, h


def validate_times(start, end, duration):
    if not (0 <= start < end <= duration + 0.01 and end - start >= 0.55):
        raise ValueError('Cue must have a valid in-video interval >=0.55s')
    return min(0.25, (end - start) / 4)


def make_cue(path, genre, rect):
    if genre not in PALETTES:
        raise ValueError('Unknown genre')
    _, _, w, h = validate_rect(rect)
    scale = 3
    color = tuple(bytes.fromhex(PALETTES[genre][1:]))
    canvas = Image.new('RGBA', (w * scale, h * scale), (0, 0, 0, 0))
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    inset = 12 * scale
    box = (inset, inset, w * scale - inset, h * scale - inset)
    g.rounded_rectangle(box, radius=13 * scale, outline=(*color, 170), width=6 * scale)
    glow = glow.filter(ImageFilter.GaussianBlur(9 * scale))
    canvas.alpha_composite(glow)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=13 * scale, outline=(*color, 220), width=3 * scale)
    canvas.resize((w, h), Image.Resampling.LANCZOS).save(path)


def render(source, output, genre, rect, start, end, report=None):
    if genre not in PALETTES:
        raise ValueError('Unsupported genre')
    rect = validate_rect(rect)
    source, output = Path(source), Path(output)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('Source missing or output equals source')
    before = probe(source)
    video, audio = streams(before)
    count = int(video.get('nb_frames') or 0)
    if (video.get('codec_name'), video.get('width'), video.get('height'),
        video.get('r_frame_rate'), audio.get('codec_name')) != ('h264', W, H, '30/1', 'aac') or not count:
        raise ValueError('Expected 1080x1920 H264/30fps and AAC with known frame count')
    duration = float(before['format']['duration'])
    fade = validate_times(start, end, duration)
    output.parent.mkdir(parents=True, exist_ok=True)
    cue = output.parent / (output.stem + '_focus_overlay.png')
    make_cue(cue, genre, rect)
    x, y, _, _ = rect
    graph = (f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={fade:.3f}:alpha=1,'
             f'fade=t=out:st={end-fade:.3f}:d={fade:.3f}:alpha=1[cue];'
             f'[0:v][cue]overlay={x}:{y}:shortest=1:format=auto[v]')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', source,
         '-loop', '1', '-framerate', FPS, '-i', cue, '-filter_complex', graph,
         '-map', '[v]', '-map', '0:a:0', '-map_chapters', '0',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
         '-x264-params', 'aq-mode=3:aq-strength=1.0', '-pix_fmt', 'yuv420p',
         '-frames:v', count, '-c:a', 'copy', '-movflags', '+faststart', output])
    after = probe(output)
    ov, oa = streams(after)
    if (ov['width'], ov['height'], ov['r_frame_rate'], int(ov.get('nb_frames') or 0)) != (W, H, '30/1', count):
        raise RuntimeError('Frame geometry/count changed')
    if oa['codec_name'] != 'aac' or aac_hash(source) != aac_hash(output):
        raise RuntimeError('AAC narration bitstream changed')
    if len(before.get('chapters', [])) != len(after.get('chapters', [])):
        raise RuntimeError('Chapter count changed')
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', output,
         '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    qa = {'genre': genre, 'genres_supported': len(PALETTES),
          'cue': {'rect': rect, 'start': start, 'end': end, 'fade': fade},
          'source_bytes': source.stat().st_size, 'output_bytes': output.stat().st_size,
          'resolution': [W, H], 'fps': FPS, 'frames': count,
          'duration_s': float(after['format']['duration']),
          'chapters': len(after.get('chapters', [])),
          'audio_aac_sha256': aac_hash(output), 'aac_bitstream_identical': True,
          'full_av_decode': 'PASS', 'subtitle_semantics': 'NOT VERIFIED - ASR unavailable',
          'source_rights': 'NOT VERIFIED', 'employee_approval': 'NOT GRANTED',
          'publication': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report:
        Path(report).write_text(json.dumps(qa, ensure_ascii=False, indent=2))
    return qa


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', choices=sorted(PALETTES), default='ai')
    p.add_argument('--rect', type=int, nargs=4, required=True, metavar=('X', 'Y', 'W', 'H'))
    p.add_argument('--start', type=float, required=True)
    p.add_argument('--end', type=float, required=True)
    p.add_argument('--report')
    args = p.parse_args()
    print(json.dumps(render(args.source, args.output, args.genre, args.rect,
                            args.start, args.end, args.report), ensure_ascii=False))
