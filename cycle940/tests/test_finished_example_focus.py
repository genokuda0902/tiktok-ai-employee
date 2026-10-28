import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import finished_example_focus as m

@pytest.mark.parametrize('genre',list(m.GENRES))
def test_ten_genre_render(genre):
    image=m.make_frame(0,genre)
    assert image.size==(1080,1445)
    assert image.mode=='RGB'

def test_timed_phases():
    assert [m.stage(i) for i in [0,28,29,57,58,86]]==[0,0,1,1,2,2]
    with pytest.raises(ValueError):m.stage(87)

def test_fails_closed(tmp_path):
    with pytest.raises(ValueError):m.guard('unknown','0'*64)
    with pytest.raises(ValueError):m.guard('ai_work','bad')
    with pytest.raises(FileNotFoundError):m.run(tmp_path/'missing',tmp_path/'o.mp4',tmp_path/'tmp','ai_work','0'*64)
    src=tmp_path/'test.mp4';src.write_bytes(b'not a video')
    with pytest.raises(RuntimeError,match='SOURCE_SHA_MISMATCH'):
        m.run(src,tmp_path/'o.mp4',tmp_path/'tmp','ai_work','0'*64)

def test_publication_guard():
    assert m.SAFE_Y<=1450
    assert m.POLICY=='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    assert m.START==174 and m.COUNT==87 and m.FRAMES==691
