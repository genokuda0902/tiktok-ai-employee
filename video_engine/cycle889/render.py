"""Re-render inherited MP4 with pause-aware captions; review only."""
import argparse
import json
import subprocess
from pathlib import Path
from pause_aware import build


def run(source: Path, source_ass: Path, destination: Path, work: Path) -> dict:
    source, source_ass, destination, work = map(Path, (source, source_ass, destination, work))
    if not source.is_file() or not source_ass.is_file():
        raise FileNotFoundError('missing inherited review input')
    if source.resolve() == destination.resolve():
        raise ValueError('source must never be overwritten')
    work.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(source)]))
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['width'], v['height'], v['r_frame_rate'], a['codec_name'], a['sample_rate']) != (1080, 1920, '30/1', 'aac', '48000'):
        raise ValueError('requires 1080x1920 30fps H264/AAC 48kHz input')
    duration = float(info['format']['duration'])
    log = work / 'silencedetect.log'
    cmd = ['ffmpeg', '-hide_banner', '-i', str(source), '-af', 'silencedetect=noise=-38dB:d=0.2', '-f', 'null', '-']
    with log.open('w') as f:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=f, check=True)
    ass = work / 'pause_aware.ass'
    metrics = build(source_ass, log, ass, duration)
    vf = f'drawbox=x=72:y=1480:w=936:h=152:color=0x040f21:t=fill,ass={ass.as_posix()}'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-y', '-i', str(source),
                    '-vf', vf, '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '19', '-threads', '2', '-pix_fmt', 'yuv420p',
                    '-c:a', 'copy', '-movflags', '+faststart', str(destination)], check=True)
    return metrics


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('source_ass', type=Path)
    p.add_argument('destination', type=Path)
    p.add_argument('work', type=Path)
    args = p.parse_args()
    print(json.dumps(run(args.source, args.source_ass, args.destination, args.work), ensure_ascii=False, indent=2))
