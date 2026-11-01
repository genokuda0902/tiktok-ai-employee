import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import pytest
from proof_focus import proof_percent,alpha_for,overlay,validate,COLORS,FRAME_COUNT,SIZE

def test_math(): assert proof_percent(44,54)==81.5
@pytest.mark.parametrize('a,b',[(0,0),(-1,54),(55,54),(44,-1),(2.2,5)])
def test_bad_counts(a,b):
    with pytest.raises(ValueError): proof_percent(a,b)
def test_bounds(): assert validate()
def test_opacity(): assert alpha_for(0)<alpha_for(6)==alpha_for(7)==1.0 and alpha_for(23)<1
@pytest.mark.parametrize('i',[0,6,7,18,23])
def test_frame(i):
    im=overlay(i)
    assert im.size==SIZE and im.mode=='RGBA' and im.getbbox() is not None
@pytest.mark.parametrize('genre',list(COLORS))
def test_genre(genre): assert overlay(10,genre).size==SIZE
def test_unknown_genre():
    with pytest.raises(ValueError): overlay(0,'unknown')
def test_bad_index():
    with pytest.raises(ValueError): alpha_for(FRAME_COUNT)
