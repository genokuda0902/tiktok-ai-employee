import json
import sys
from pathlib import Path
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from render import validate, eased, position_on_polyline, apply_cue, composite_glow

CFG=json.loads((ROOT/'config/semantic_cues.json').read_text(encoding='utf-8'))


def test_ten_genres():
    assert len(json.loads((ROOT/'config/genres.json').read_text(encoding='utf-8'))['genres'])==10


def test_36_frames():
    assert validate(CFG)==36


def test_ease_endpoints():
    assert eased(0)==0 and eased(1)==1 and eased(.5)==.5


def test_path_endpoints():
    path=CFG['animations'][0]['path']
    assert position_on_polyline(path,0)==tuple(path[0])
    assert position_on_polyline(path,1)==tuple(path[-1])


def test_unmodified_frame_outside_cues():
    f=np.zeros((1920,1080,3),dtype=np.uint8)
    assert np.array_equal(apply_cue(f,30,CFG),f)


def test_changes_during_current():
    f=np.zeros((1920,1080,3),dtype=np.uint8)
    assert np.count_nonzero(apply_cue(f,250,CFG))>0


def test_changes_during_led():
    f=np.zeros((1920,1080,3),dtype=np.uint8)
    assert np.count_nonzero(apply_cue(f,268,CFG))>0


def test_caption_region_unchanged():
    f=np.random.default_rng(753).integers(0,255,size=(1920,1080,3),dtype=np.uint8)
    for idx in (245,260,270,279):
        out=apply_cue(f,idx,CFG)
        assert np.array_equal(out[CFG['caption_safe_y']:],f[CFG['caption_safe_y']:])


def test_config_rejects_overlap():
    cfg=json.loads(json.dumps(CFG))
    cfg['animations'][1]['start_frame']=260
    with pytest.raises(AssertionError):
        validate(cfg)


def test_config_rejects_unsafe_position():
    cfg=json.loads(json.dumps(CFG))
    cfg['animations'][1]['center']=[100,1500]
    with pytest.raises(AssertionError):
        validate(cfg)


def test_no_network_dependencies():
    import inspect
    import render
    code=inspect.getsource(render)
    assert 'requests' not in code and 'urllib' not in code
