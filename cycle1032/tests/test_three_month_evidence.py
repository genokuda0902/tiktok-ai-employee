import importlib.util
from pathlib import Path
import pytest
M=Path(__file__).resolve().parents[1]/'source'/'three_month_evidence.py'
spec=importlib.util.spec_from_file_location('three_month_evidence',M)
m=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=m
spec.loader.exec_module(m)

def test_ten_genres(): assert len(m.GENRES)==10

def test_arithmetic_and_missing_june_fixed():
    x=m.DEFAULT_EXAMPLE
    assert x.categories==('4月','5月','6月')
    assert x.series_a[2]==18 and x.series_b[2]==12
    assert sum(x.series_a)==46 and sum(x.series_b)==29

@pytest.mark.parametrize('beat',[0,1,2])
def test_panel_safe_and_visible(beat):
    im=m.draw_panel(m.DEFAULT_EXAMPLE,beat)
    assert im.size==(1080,1920)
    assert im.getbbox()[3]<=m.SAFE_SUBTITLE_Y
    assert im.getpixel((500,1000))[3]>0

@pytest.mark.parametrize('genre',sorted(m.GENRES))
def test_shared_ten_genre_panel(genre):
    x=m.DEFAULT_EXAMPLE
    demo=m.Evidence(genre,x.categories,x.series_a,x.series_b,'A','B',True,'fictional_educational_example')
    assert m.draw_panel(demo,0).getbbox() is not None

def test_bad_genre():
    with pytest.raises(ValueError):
        m.Evidence('not-a-genre',('1','2','3'),(1,2,3),(2,3,4),'A','B',True,'fictional_educational_example').validate()

def test_unapproved_provenance_fails():
    x=m.DEFAULT_EXAMPLE
    with pytest.raises(ValueError):
        m.Evidence(x.genre,x.categories,x.series_a,x.series_b,x.label_a,x.label_b,False,'unknown').validate()

def test_beat_graph():
    assert "between(n,342,370)" in m.graph(m.BEATS)
    assert m.BEATS[2][1]<m.SAFE_SUBTITLE_Y
    with pytest.raises(ValueError):m.graph(((1,2),(4,5),(6,7)))

def test_fail_closed(tmp_path):
    with pytest.raises(ValueError):
        m.render(tmp_path/'missing.mp4',tmp_path/'out.mp4',tmp_path/'qa.json','0'*64,review_only=False)
    with pytest.raises(ValueError):
        m.render(tmp_path/'missing.mp4',tmp_path/'out.mp4',tmp_path/'qa.json','0'*64,genre='health_lifestyle',review_only=True)
