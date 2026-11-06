from pathlib import Path
import importlib.util
p=Path(__file__).with_name('render.py')
spec=importlib.util.spec_from_file_location('review_renderer',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def test_three_scenes(): assert len(m.SCENES)==3
def test_no_private_assets(): assert all('IMG_' not in str(s) for s in m.SCENES)
def test_review_only(): assert 'REVIEW ONLY' in p.read_text()
