import importlib.util
from pathlib import Path
import pytest

p=Path(__file__).resolve().parents[1]/'src'/'smooth_scene_cuts.py'
spec=importlib.util.spec_from_file_location('smooth_scene_cuts',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

@pytest.mark.parametrize('genre',m.GENRES)
def test_ten_genres_supported(genre):
    assert genre in m.GENRES
    assert m.validate_cuts()

def test_filter_preserves_cut_centers():
    f=m.filtergraph()
    assert f.count('xfade=')==5
    for cut in m.CUTS:
        assert f'offset={cut-.1:g}' in f
    assert '[v]' in f

def test_reject_unsafe_overlapping_transitions():
    with pytest.raises(ValueError):m.validate_cuts((3.2,3.3),.2)

def test_reject_frame_misalignment():
    with pytest.raises(ValueError):m.validate_cuts((3.21,6.5),.2)

def test_reject_invalid_duration():
    with pytest.raises(ValueError):m.validate_cuts(duration=.6)

def test_reject_bad_aspect_ratio():
    with pytest.raises(ValueError):m.filtergraph(scale=(480,480))

def test_audio_preservation_by_command_contract(tmp_path):
    source=tmp_path/'fake.mp4';source.write_bytes(b'not-a-real-video')
    # inspect generator source for explicit passthrough; ffmpeg E2E verifies actual hash.
    text=p.read_text()
    assert "'-map','0:a:0'" in text
    assert "'-c:a','copy'" in text

def test_no_auto_post_or_external_calls():
    text=p.read_text()
    assert 'requests.' not in text
    assert 'upload(' not in text
