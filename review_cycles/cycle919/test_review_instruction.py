import importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent/'review_instruction.py'
spec=importlib.util.spec_from_file_location('review_instruction',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_presets():assert m.validate_presets()
def test_dimensions():assert m.render(0).size==(1080,1160)
def test_beats_are_distinct():
 import numpy as np
 a=np.array(m.render(10).resize((270,290)))
 b=np.array(m.render(44).resize((270,290)))
 c=np.array(m.render(80).resize((270,290)))
 assert np.abs(a.astype('int16')-b.astype('int16')).mean()>1
 assert np.abs(b.astype('int16')-c.astype('int16')).mean()>1

def test_all_genres_render():
 for genre in m.GENRES:assert m.render(75,genre).size==(1080,1160)
def test_reject_bad_inputs():
 import pytest
 with pytest.raises(ValueError):m.render(-1)
 with pytest.raises(ValueError):m.render(87)
 with pytest.raises(ValueError):m.render(1,'fake')
def test_safe_review_only():
 source=P.read_text()
 for prohibited in ['requests.post(', 'publish_video(', 'upload_video(', 'merge_pull_request(']:
  assert prohibited not in source
