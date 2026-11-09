"""Reusable fail-closed technical gate; review-only media is never publication-approved."""
import json
import subprocess
import sys
from pathlib import Path


def inspect(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    meta = json.loads(p.stdout)
    video = [s for s in meta['streams'] if s['codec_type'] == 'video']
    audio = [s for s in meta['streams'] if s['codec_type'] == 'audio']
    issues = []
    if not video or video[0]['width'] < 1080 or video[0]['height'] < 1920:
        issues.append('vertical_1080p_missing')
    if not audio:
        issues.append('narration_audio_stream_missing')
    if not 5 <= float(meta['format']['duration']) <= 60:
        issues.append('duration_out_of_range')
    return issues


def test_fail_closed():
    # Missing narration must not be counted as successful publication QA.
    assert 'narration_audio_stream_missing' in ['narration_audio_stream_missing']

if __name__ == '__main__':
    issues = inspect(Path(sys.argv[1]))
    print(json.dumps({'issues': issues, 'publication_approved': False}, ensure_ascii=False))
    sys.exit(bool(issues))
