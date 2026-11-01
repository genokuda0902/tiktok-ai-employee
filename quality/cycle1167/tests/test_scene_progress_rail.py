import importlib.util
from pathlib import Path
import numpy as np
import pytest

P=Path(__file__).resolve().parents[1]/'code'/'scene_progress_rail.py'
spec=importlib.util.spec_from_file_location('scene_progress_rail',P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_baseline(): assert m.validate()
def test_ten_genres(): assert len(m.GENRE_COLORS)==10

@pytest.mark.parametrize('genre',list(m.GENRE_COLORS))
def test_palette_images(genre):
    im=m.draw_rail(.5,m.GENRE_COLORS[genre])
    assert im.size==m.ROI[2:]
    a=np.asarray(im)
    assert a.shape==(18,620,4)
    assert a[:,:,3].max()<=205 and a[:,:,3].min()==0

def test_reset_at_each_cut():
    for s in m.SCENE_STARTS[1:]:
        i,p=m.scene_for_frame(s)
        assert p==0
        j,previous=m.scene_for_frame(s-1)
        assert previous==1 and i==j+1

def test_first_last():
    assert m.scene_for_frame(0)==(0,0)
    assert m.scene_for_frame(674)==(7,1)

def test_progress_is_monotonic_within_scene():
    for start,end in zip(m.SCENE_STARTS,m.SCENE_ENDS):
        p=[m.scene_for_frame(i)[1] for i in range(start,end)]
        assert p[0]==0 and p[-1]==1
        assert all(b>=a for a,b in zip(p,p[1:]))

def test_safe_strip_validation():
    with pytest.raises(ValueError):m.validate(roi=(130,1450,620,18))
    with pytest.raises(ValueError):m.validate(roi=(130,1630,620,18))

def test_bad_frame_and_bad_genre(tmp_path):
    with pytest.raises(ValueError):m.scene_for_frame(-1)
    with pytest.raises(ValueError):m.scene_for_frame(675)
    with pytest.raises(ValueError):m.write_overlays(tmp_path,'unknown')

def test_transparency_and_progress():
    c=m.GENRE_COLORS['ai-work']
    zero=np.asarray(m.draw_rail(0,c))
    half=np.asarray(m.draw_rail(.5,c))
    full=np.asarray(m.draw_rail(1,c))
    assert np.count_nonzero(zero[7:10,:,3]>150)==0
    assert np.count_nonzero(half[7:10,:,3]>150)<np.count_nonzero(full[7:10,:,3]>150)
    assert np.count_nonzero(full[7:10,:,3]>150)>1000

def test_short_synthetic_overlay(tmp_path):
    starts=(0,10,20)
    m.write_overlays(tmp_path,'learning',starts,30)
    assert len(list(tmp_path.glob('rail_*.png')))==30
    a=np.asarray(m.Image.open(tmp_path/'rail_00009.png'))
    b=np.asarray(m.Image.open(tmp_path/'rail_00010.png'))
    assert a[8,:,3].sum()>b[8,:,3].sum()
