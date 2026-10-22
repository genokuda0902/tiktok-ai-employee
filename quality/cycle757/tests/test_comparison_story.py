import importlib.util
from pathlib import Path
from PIL import Image
import pytest

P=Path(__file__).parents[1]/'src/comparison_story.py'
s=importlib.util.spec_from_file_location('comparison_story',P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

@pytest.mark.parametrize('genre',list(m.COLORS))
def test_all_genres_render(genre):
    pic=Image.new('RGB',(1600,1000),'white')
    f=m.frame(40,pic,genre)
    assert f.size==(540,960)
    assert f.getpixel((270,440)) != f.getpixel((1,1))

def test_data_matches_spoken_numbers():assert m.verify_data()
def test_reject_wrong_sum():
    with pytest.raises(ValueError):m.verify_data({'1月':1,'2月':2,'3月':3,'4月':4})
def test_important_bounds():assert m.verify_bounds(m.boxes())
def test_reject_unsafe_bounds():
    with pytest.raises(ValueError):m.verify_bounds({'bad':(0,0,300,500)})
def test_frames_and_timing():
    assert (m.START_FRAME,m.END_FRAME,m.FRAMES)==(493,604,111)
    assert m.START_FRAME/m.FPS>16 and m.END_FRAME/m.FPS<21
@pytest.mark.parametrize('index',[-1,111])
def test_reject_out_of_range(index):
    with pytest.raises(ValueError):m.frame(index,Image.new('RGB',(1600,1000)))
