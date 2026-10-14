import importlib.util
from pathlib import Path
import subprocess, json, wave, hashlib
import pytest

spec=importlib.util.spec_from_file_location('cycle566_render',Path(__file__).with_name('render.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_scene_cues():
    assert len(m.CUES)==7
    assert all(a<b for a,b in zip(m.CUES,m.CUES[1:]))
    assert m.CUES[-1]<m.DURATION

def test_caption_timeline():
    assert m.CAPTIONS[0][0]==0 and m.CAPTIONS[-1][1]==m.DURATION
    assert all(b>a and len(s)<=30 for a,b,s in m.CAPTIONS)
    assert all(a[1]==b[0] for a,b in zip(m.CAPTIONS,m.CAPTIONS[1:]))

def test_score_non_silent_and_fade(tmp_path):
    f=tmp_path/'original.wav';m.score(f)
    with wave.open(str(f)) as w:
        assert w.getnframes()==882000 and w.getframerate()==44100
        import array
        pcm=array.array('h',w.readframes(w.getnframes()))
    assert max(abs(v) for v in pcm)>1000
    assert max(abs(v) for v in pcm)<32767
    assert abs(pcm[0])==0 and abs(pcm[-1])<100

def test_visual_subtitles(tmp_path):
    p=tmp_path/'captions.srt';m.make_srt(p)
    t=p.read_text()
    assert t.count('-->')==8 and 'SUM' in t and '720' in t

def test_render_metadata_and_audio_is_new(tmp_path):
    source=Path('/mnt/data/cycle565/cycle565_audio_seam_REVIEW_ONLY.mp4')
    if not source.exists(): pytest.skip('previous local MP4 unavailable')
    out=tmp_path/'preview.mp4'; data=m.render(source,out)
    assert out.stat().st_size>100000
    assert data['inherited_audio_used'] is False
    assert data['japanese_narration']=='NOT_GENERATED'
    assert hashlib.sha256(out.read_bytes()).hexdigest()==data['output_sha256']
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
    assert any(s['codec_type']=='video' and s['width']==1080 and s['height']==1920 for s in j['streams'])
    assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in j['streams'])
    assert any(s['codec_type']=='subtitle' for s in j['streams'])
    assert abs(float(j['format']['duration'])-20)<0.05
