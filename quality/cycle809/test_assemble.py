import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('cycle809_assembler',Path(__file__).with_name('assemble_mp4.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_frame_allocation():
    data={'sentences':[{'seconds':3.0}]*8}
    assert m.frame_counts(data,720)==[90]*8
    assert sum(m.frame_counts(data,721))==721

def test_invalid_scene_count():
    try:
        m.frame_counts({'sentences':[{'seconds':3.0}]*7},630)
    except ValueError:pass
    else:raise AssertionError('accepted seven scenes')

def test_approval_gate_in_source():
    src=Path(__file__).with_name('assemble_mp4.py').read_text()
    assert "HUMAN_REVIEW" in src
    assert 'auto_post' not in src
