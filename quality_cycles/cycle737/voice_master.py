"""cycle737: reusable Japanese narration speech-clarity master.

Video H.264 bitstream is copied unchanged; FFmpeg only, no network/TTS.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def run(*args):
    p = subprocess.run(list(map(str, args)), capture_output=True, text=True, check=False)
    if p.returncode:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(map(str, args))}\n{p.stderr[-2500:]}")
    return p.stdout, p.stderr


def probe(path):
    out, _ = run('ffprobe', '-v', 'error', '-show_entries',
                 'format=duration:stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels',
                 '-of', 'json', path)
    return json.loads(out)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()


def loudness_stats(path, prefilter=''):
    af = (prefilter + ',' if prefilter else '') + 'loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json'
    _, err = run('ffmpeg', '-hide_banner', '-nostats', '-i', path, '-vn', '-af', af, '-f', 'null', '-')
    blocks = re.findall(r'\{\s*"input_i"\s*:\s*".*?\}', err, re.S)
    if not blocks:
        raise RuntimeError('FFmpeg loudnorm stats missing')
    return json.loads(blocks[-1])


def video_bitstream_sha(path):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                          '-c:v', 'copy', '-f', 'h264', '-'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    h = hashlib.sha256()
    for b in iter(lambda: p.stdout.read(1024 * 1024), b''):
        h.update(b)
    _, err = p.communicate()
    if p.returncode:
        raise RuntimeError(err.decode()[-1000:])
    return h.hexdigest()


def master(src, dst):
    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Gentle speech EQ; do not add compression to already-mastered audio.
    pre = 'highpass=f=85,equalizer=f=2800:t=q:w=1.0:g=1.2'
    original_duration = float(probe(src)['format']['duration'])
    stats = loudness_stats(src, pre)
    args = (f'linear=true:measured_I={stats["input_i"]}:measured_TP={stats["input_tp"]}:'
            f'measured_LRA={stats["input_lra"]}:measured_thresh={stats["input_thresh"]}:'
            f'offset={stats["target_offset"]}')
    filt = f'{pre},loudnorm=I=-16:TP=-1.5:LRA=7:{args},aresample=48000'
    run('ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', src,
        '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'copy', '-c:a', 'aac',
        '-b:a', '192k', '-ar', '48000', '-ac', '1', '-af', filt,
        '-t', f'{original_duration:.6f}', '-movflags', '+faststart', dst)
    return {'filter': filt, 'first_pass': stats,
            'source_sha256': sha(src), 'output_sha256': sha(dst),
            'source_video_bitstream_sha256': video_bitstream_sha(src),
            'output_video_bitstream_sha256': video_bitstream_sha(dst),
            'source': probe(src), 'output': probe(dst)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--report', required=True)
    a = ap.parse_args()
    info = master(a.input, a.output)
    Path(a.report).write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({'output': a.output,
                      'video_copy': info['source_video_bitstream_sha256'] ==
                                    info['output_video_bitstream_sha256']}, ensure_ascii=False))
