import importlib.util
from pathlib import Path
import pytest
M=Path(__file__).resolve().parents[1]/'source'/'correction_proof.py'
spec=importlib.util.spec_from_file_location('correction_proof',M)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def test_ten_genres(): assert len(m.GENRES)==10
@pytest.mark.parametrize('genre',sorted(m.GENRES))
def test_panels(genre):
 for beat in (1,2):
  im=m.panel(genre,beat)
  assert im.size==(1080,1920)
  assert im.getbbox() is not None
def test_unknown_genre():
 with pytest.raises(ValueError):m.panel('private',1)
def test_arithmetic_proof():
 assert sum((12,16,18))==46
 assert m.GENRES['ai_work'][3:] == ('45','46')
def test_safe_window():
 assert 14.0<m.START<m.MID<m.END<17.0
 assert 'overlay=x=0:y=0' in m.filter_graph(m.START,m.MID,m.END)
def test_bad_window():
 with pytest.raises(ValueError):m.filter_graph(2,1,3)
def test_fail_closed_missing_source(tmp_path):
 with pytest.raises(ValueError):m.render(tmp_path/'missing.mp4',tmp_path/'out.mp4',tmp_path/'qa.json','ai_work','0'*64,review_only=False)
