"""Mix quiet synthetic UI cues with inherited narration; video stream-copy.
Review-only. No auto-posting, uploads, rights claims or third-party services.
"""
import argparse
import json
import subprocess
from pathlib import Path
from sfx_generator import make_cues

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))

def render(source: Path, destination: Path, work: Path):
    source, destination, work = Path(source), Path(destination), Path(work)
    if not source.is_file() or source.resolve() == destination.resolve():
        raise ValueError('source must exist and must not be overwritten')
    info = probe(source)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['codec_name'], v['width'], v['height'], v['r_frame_rate'], a['codec_name'], a['sample_rate']) != ('h264', 1080, 1920, '30/1', 'aac', '48000'):
        raise ValueError('input must be 1080x1920 H264 30fps + AAC 48kHz')
    duration = float(info['format']['duration'])
    work.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cues = work / 'original_ui_cues.wav'
    metrics = make_cues(cues, duration)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-y',
           '-i', str(source), '-i', str(cues),
           '-filter_complex', '[0:a]volume=0.94[n];[n][1:a]amix=inputs=2:duration=first:normalize=0:dropout_transition=0[a]',
           '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
           '-ar', '48000', '-ac', '1', '-movflags', '+faststart', str(destination)]
    subprocess.run(cmd, check=True)
    return {'source': str(source), 'output': str(destination), 'cues': metrics,
            'narration_gain': 0.94, 'video_mode': 'stream-copy',
            'approval': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('destination', type=Path)
    p.add_argument('work', type=Path)
    args = p.parse_args()
    print(json.dumps(render(args.source, args.destination, args.work), ensure_ascii=False, indent=2))
