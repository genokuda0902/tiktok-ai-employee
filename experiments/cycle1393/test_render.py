from pathlib import Path
import subprocess, json

ROOT=Path(__file__).parent
VIDEO=ROOT/'cycle1393_REVIEW_ONLY.mp4'

def test_video_has_visual_and_no_claimed_audio():
    assert VIDEO.exists()
    p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height','-of','json',str(VIDEO)],capture_output=True,text=True,check=True)
    streams=json.loads(p.stdout)['streams']
    assert any(s.get('codec_type')=='video' and s.get('width')==720 and s.get('height')==1280 for s in streams)
    assert not any(s.get('codec_type')=='audio' for s in streams), 'Review-only video unexpectedly has audio; inspect it before approval'

def test_caption_source_and_motion():
    source=(ROOT/'render.py').read_text(encoding='utf-8')
    assert 'Burn-in timed captions' in source
    assert 'Moving pointer' in source
    assert '公開不可' in source
