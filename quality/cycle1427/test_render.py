from pathlib import Path
import json, subprocess
P=Path(__file__).resolve().parent
def test_files():
    assert (P/'cycle1427_REVIEW_ONLY.mp4').stat().st_size>10000
    assert (P/'captions.srt').exists()
def test_tracks():
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P/'cycle1427_REVIEW_ONLY.mp4')]))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    a=next(s for s in d['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==(1080,1920)
    assert v['codec_name']=='h264' and a['codec_name']=='aac'
    assert 14.9<float(d['format']['duration'])<15.1
def test_fail_closed():
    q=json.loads((P/'qa.json').read_text())
    assert not q['japanese_narration'] and not q['speech_synced_captions'] and not q['publication_approved']
def test_no_false_audio_claim():
    q=json.loads((P/'qa.json').read_text(encoding='utf-8'))
    assert q['audio']=='original synthesized cue only'
    assert q['publication_approved'] is False
