"""Synthetic-only CI: never accesses or uploads the real review MP4."""
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'narration_loudness.py'
spec = importlib.util.spec_from_file_location('narration_loudness', P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def check(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def h264_hash(p):
    x = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-map', '0:v:0',
                        '-c:v', 'copy', '-f', 'h264', '-'], check=True, stdout=subprocess.PIPE)
    return hashlib.sha256(x.stdout).hexdigest()


def probe(p):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
             '-show_format', '-of', 'json', str(p)]))


def main():
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / 'in.mp4', Path(d) / 'out.mp4'
        check(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-f', 'lavfi', '-i', 'color=c=#0c1726:s=1080x1920:r=30:d=3',
               '-f', 'lavfi', '-i', 'sine=frequency=320:sample_rate=48000:duration=3',
               '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '128k', '-shortest', str(src)])
        report = mod.master(src, dst, genre='learning')
        check(['ffmpeg', '-v', 'error', '-xerror', '-i', str(dst), '-f', 'null', '-'])
        before, after = probe(src), probe(dst)
        v = [s for s in after['streams'] if s['codec_type'] == 'video'][0]
        a = [s for s in after['streams'] if s['codec_type'] == 'audio'][0]
        assert (v['width'], v['height'], v['codec_name']) == (1080, 1920, 'h264')
        assert a['codec_name'] == 'aac' and a['sample_rate'] == '48000'
        assert h264_hash(src) == h264_hash(dst), 'H264 packet stream changed'
        assert abs(report['after_lufs'] + 16) <= .4, report
        assert report['after_true_peak_dbtp'] <= -1.35, report
        assert before['streams'][0]['codec_name'] == v['codec_name']
        print('PASS synthetic 3s 1080x1920, full decode, audio target, H264 bitstream identical')


if __name__ == '__main__':
    main()
