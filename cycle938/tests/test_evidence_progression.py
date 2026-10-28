import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import evidence_progression as m

@pytest.mark.parametrize('genre',list(m.GENRES))
def test_ten_genres(genre):
 image=m.render_frame(0,genre)
 assert image.size==(1080,1445)
 assert image.getpixel((0,0))==(5,20,35)

def test_phases():
 assert [m.phase(i) for i in (0,28,29,57,58,86)]==[0,0,1,1,2,2]

def test_fail_closed(tmp_path):
 for bad in ('','ai_works','../other'):
  with pytest.raises(ValueError):m.check(bad)
 with pytest.raises(ValueError):m.render_frame(0,draft='1; rm -rf')
 with pytest.raises(ValueError):m.phase(87)
 with pytest.raises(FileNotFoundError):m.render('/missing',tmp_path/'never.mp4',tmp_path,'ai_work','0'*64)
 src=tmp_path/'sample.mp4';src.write_bytes(b'not a real movie')
 with pytest.raises(RuntimeError,match='SOURCE_SHA_MISMATCH'):
  m.render(src,tmp_path/'out.mp4',tmp_path/'tmp','ai_work','0'*64)

def test_policy():
 assert m.POLICY=='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
 assert m.SAFE_Y<=1450
 assert m.END-m.START==87
 assert m.NFRAMES==691
