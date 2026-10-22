"""Genre-independent QA for the cycle756 mobile-safe result-first hook."""
import importlib.util
from pathlib import Path
import pytest
from PIL import Image
SRC=Path(__file__).resolve().parents[1]/'src'/'mobile_hero.py'
spec=importlib.util.spec_from_file_location('mobile_hero',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_ten_genres():
    assert len(m.GENRE_COLORS)==10
    assert len(set(m.GENRE_COLORS.values()))==10

@pytest.mark.parametrize('genre',list(m.GENRE_COLORS))
def test_safe_layout_all_genres(genre):
    assert m.verify_important_bounds(m.important_boxes())
    sample=Image.new('RGB',(1600,1000),'white')
    base=m.compose_static(sample,genre)
    assert base.size==(1080,1920)
    first=m.frame_image(0,base,genre)
    mid=m.frame_image(15,base,genre)
    assert first.size==mid.size==(1080,1920)
    assert first.getbbox() is not None

def test_numbers_exact():
    assert m.sum_sales()==650000
    with pytest.raises(ValueError):m.sum_sales([1,-1])
    with pytest.raises(ValueError):m.sum_sales([True,1])

def test_unsafe_layout_rejected():
    with pytest.raises(ValueError):m.verify_important_bounds({'bad':(900,100,1010,200)})

def test_missing_or_unknown_inputs():
    with pytest.raises(ValueError):m.compose_static(Image.new('RGB',(100,100)), 'ai_work')
    with pytest.raises(ValueError):m.compose_static(Image.new('RGB',(1600,1000)), 'unknown')

def test_reveal_and_fade():
    base=m.compose_static(Image.new('RGB',(1600,1000)),'ai_work')
    a=m.frame_image(0,base);b=m.frame_image(15,base);c=m.frame_image(95,base)
    assert a.getpixel((125,900))!=b.getpixel((125,900))
    assert c.getchannel('A').getextrema()==(0,0)
