from pathlib import Path
from PIL import Image
from slide_layout import REGIONS, make_slide

def test_non_overlapping_regions():
    h,b,c = REGIONS["heading"],REGIONS["body"],REGIONS["caption"]
    assert h[3] < b[1] and b[3] < c[1]

def test_slide_dimensions(tmp_path):
    p=tmp_path/"slide.png"
    make_slide(1,"目的を先に伝える","最初の3秒で理由を明確に","結論を先に。",p)
    assert Image.open(p).size == (1080,1920)
