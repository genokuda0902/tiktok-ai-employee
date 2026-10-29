import importlib.util
from pathlib import Path
import numpy as np
import pytest
spec=importlib.util.spec_from_file_location('focus',Path(__file__).resolve().parents[1]/'src'/'scene_focus_lock.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
BASE={'genre':'ai_work','source_sha256':'a'*64,'source_scene':2,'caption':'まず、繰り返している作業を書き出そう。','active_step':1,'geometry_reviewed':True}

def test_manifest(): assert m.validate(BASE)
@pytest.mark.parametrize('genre',m.GENRES)
def test_genres(genre): assert m.validate({**BASE,'genre':genre})
@pytest.mark.parametrize('patch',[
 {'geometry_reviewed':False},{'active_step':2},{'source_scene':3},{'caption':'合計を確認'},
 {'source_sha256':''},{'genre':'unknown'}])
def test_fail_closed(patch):
    with pytest.raises(ValueError): m.validate({**BASE,**patch})
def test_outside_window():
    a=np.zeros((1920,1080,3),dtype=np.uint8)
    b=np.ones_like(a)*200
    assert np.array_equal(m.focus_frame(a,b,3.0),a)
    assert np.array_equal(m.focus_frame(a,b,5.9),a)
def test_caption_protection():
    a=np.zeros((1920,1080,3),dtype=np.uint8)
    b=np.ones_like(a)*200
    out=m.focus_frame(a,b,4.8)
    assert np.array_equal(out[m.CAPTION_TOP:],a[m.CAPTION_TOP:])
    assert out[700,300].mean()>100
