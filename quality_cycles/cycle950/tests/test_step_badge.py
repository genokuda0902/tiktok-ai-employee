"""Offline tests; no user media or publishing API needed."""
import importlib.util
from pathlib import Path
import sys
import pytest

path=Path(__file__).resolve().parents[1]/'step_badge.py'
spec=importlib.util.spec_from_file_location('step_badge',path)
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

@pytest.mark.parametrize('genre',list(mod.GENRE_ACCENTS))
def test_genres(genre):
    im=mod.render_badge(200,genre)
    assert im.size==(320,130) and im.mode=='RGBA' and im.getbbox()

@pytest.mark.parametrize('frame,scene',[(0,1),(86,1),(87,2),(173,2),
    (174,3),(347,4),(348,5),(434,5),(435,6),(521,6),
    (522,7),(608,7),(609,8),(690,8)])
def test_edges(frame,scene):
    actual,progress=mod.scene_for_frame(frame)
    assert actual==scene and 0<=progress<1

@pytest.mark.parametrize('frame',[-1,691,10000])
def test_invalid_frame(frame):
    with pytest.raises(ValueError): mod.scene_for_frame(frame)

def test_unsupported_genre():
    with pytest.raises(ValueError): mod.render_badge(0,'unknown')

def test_geometry():
    mod.BadgeConfig().validate()
    assert mod.BADGE_Y+mod.BADGE_H<=250
    assert mod.SCENE_EDGES[-1]==mod.FRAME_COUNT

def test_animated_and_changes_scene():
    a=mod.render_badge(0).tobytes()
    b=mod.render_badge(45).tobytes()
    c=mod.render_badge(87).tobytes()
    assert a!=b!=c

def test_no_posting():
    source=path.read_text()
    for term in ('requests.post','tiktok.upload','publish_video','auto_post'):
        assert term not in source
