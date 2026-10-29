import importlib.util
from pathlib import Path
import numpy as np
import pytest
from PIL import Image
spec=importlib.util.spec_from_file_location('cinematic',Path(__file__).with_name('cinematic_scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASE={'genre':'ai_work','source_sha256':'a'*64,'asset_sha256':'b'*64,
      'asset_origin':'user_library_generated_image','asset_review_only':True,
      'publication_approved':False,'geometry_reviewed':True,'source_scene':2,
      'caption':'まず、繰り返している作業を書き出そう。'}

def test_validate(): assert m.validate(BASE)
@pytest.mark.parametrize('key,value',[
 ('source_sha256',''),('asset_sha256','x'*64),('asset_origin','unknown'),
 ('asset_review_only',False),('publication_approved',True),('geometry_reviewed',False),
 ('source_scene',3),('caption','合計を確認'),('genre','unknown'),('genre','finance')])
def test_fail_closed(key,value):
    with pytest.raises(ValueError):m.validate({**BASE,key:value})
@pytest.mark.parametrize('genre',m.GENRES)
def test_genre_layout_configuration(genre):
    assert len(m.GENRE_STEPS[genre])==3
    assert all(len(x)<15 for x in m.GENRE_STEPS[genre])

def test_scene_protects_caption_and_header():
    frame=np.zeros((1920,1080,3),dtype=np.uint8)
    photo=Image.new('RGB',(1080,1490),(70,90,110))
    out=m.composite(frame,photo,4.8)
    assert np.array_equal(out[m.SUBTITLE_Y:],frame[m.SUBTITLE_Y:])
    assert out[50,100].mean()>0  # replacement has its own full header
    assert np.mean(out[300:500,100:900])>10

def test_outside_window_unchanged():
    frame=np.full((1920,1080,3),77,dtype=np.uint8)
    photo=Image.new('RGB',(1080,1490),'black')
    assert m.composite(frame,photo,2.5) is frame
    assert m.composite(frame,photo,6.0) is frame

def test_first_step_not_visible_before_start():
    photo=Image.new('RGB',(1080,1490),(70,90,110))
    early=m.make_scene(photo,2.9)
    late=m.make_scene(photo,5.3)
    assert np.abs(early[1050:1390].astype('int16')-late[1050:1390].astype('int16')).mean()>5
