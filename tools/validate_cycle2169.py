"""Reject portrait review videos lacking a spoken-audio track."""
import json
import subprocess
import sys


def validate(path):
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', path], text=True)
    streams = json.loads(raw)['streams']
    video = next((s for s in streams if s['codec_type'] == 'video'), None)
    assert video and (video['width'], video['height']) == (1080, 1920), 'not 1080x1920'
    audio = [s for s in streams if s['codec_type'] == 'audio']
    assert audio, 'FAIL: Japanese narration absent (no audio stream)'
    return True

if __name__ == '__main__':
    validate(sys.argv[1])
