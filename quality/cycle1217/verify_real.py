"""Local verification for private review MP4; never run on GitHub CI."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def call(cmd):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def info(p):
    return json.loads(call(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                            '-show_chapters', '-of', 'json', str(p)]))


def stream_hash(p):
    return hashlib.sha256(call(['ffmpeg', '-v', 'error', '-i', str(p), '-map', '0:v:0',
                                '-c:v', 'copy', '-f', 'h264', '-'])).hexdigest()


def verify(src, dst, stats):
    before, after = info(src), info(dst)
    video = next(s for s in after['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in after['streams'] if s['codec_type'] == 'audio')
    assert video['codec_name'] == 'h264' and (video['width'], video['height']) == (1080, 1920)
    assert video['avg_frame_rate'] == '30/1' and int(video['nb_frames']) == 675
    assert audio['codec_name'] == 'aac' and int(audio['sample_rate']) == 48000
    assert audio['tags']['language'] == 'jpn'
    assert len(before['chapters']) == len(after['chapters']) == 8
    assert [c['tags'].get('title') for c in before['chapters']] == [c['tags'].get('title') for c in after['chapters']]
    assert abs(float(after['format']['duration']) - 22.5) < 0.1
    assert stream_hash(src) == stream_hash(dst)
    call(['ffmpeg', '-v', 'error', '-xerror', '-i', str(dst), '-f', 'null', '-'])
    data = json.loads(Path(stats).read_text(encoding='utf-8'))
    assert abs(data['after_lufs'] + 16) <= 0.4
    assert data['after_true_peak_dbtp'] <= -1.35
    return {
        'cycle': 1217, 'previous': 1215,
        'improvement': 'Two-pass Japanese narration loudness leveling and true-peak ceiling',
        'source': str(src), 'output': str(dst),
        'source_sha256': hashlib.sha256(Path(src).read_bytes()).hexdigest(),
        'output_sha256': hashlib.sha256(Path(dst).read_bytes()).hexdigest(),
        'output_bytes': Path(dst).stat().st_size,
        'duration_seconds': float(after['format']['duration']),
        'width': video['width'], 'height': video['height'],
        'fps': video['avg_frame_rate'], 'frames': int(video['nb_frames']),
        'video_codec': video['codec_name'], 'audio_codec': audio['codec_name'],
        'audio_sample_rate': int(audio['sample_rate']), 'audio_language': audio['tags']['language'],
        'chapters_preserved': 8, 'video_bitstream_identical': True,
        'burned_subtitles_pixel_identical': True,
        'full_av_decode': 'PASS', 'loudness': data,
        'japanese_speech_semantic_transcription': 'NOT VERIFIED - offline ASR model unavailable',
        'reference_v33_original': 'NOT ACCESSIBLE',
        'media_rights': 'NOT INDEPENDENTLY VERIFIED',
        'smartphone_hardware': 'NOT VERIFIED',
        'employee_approval': 'NOT RECEIVED',
        'publication': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'supported_genres': ['ai','business','money','learning','health','food','travel','beauty','career','life'],
        'rendered_genres': ['ai'],
        'github_ci_scope': 'Synthetic 3s MP4 and 8 unit tests; not the private full MP4'
    }


if __name__ == '__main__':
    d = verify(*map(Path, sys.argv[1:4]))
    Path(sys.argv[4]).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in d.items() if k in ('frames','duration_seconds','output_bytes','video_bitstream_identical','full_av_decode','output_sha256')}, indent=2))
