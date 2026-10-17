"""Quality gate: 10 genres, 8 timed overlays, conservative UI safety."""
import importlib.util
from pathlib import Path
from PIL import Image
import pytest

mod_path=Path(__file__).resolve().parent.parent/"micro_explainers.py"
spec=importlib.util.spec_from_file_location("micro_explainers",mod_path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_ten_genres():
    assert len(m.GENRES)==10 and len(set(m.GENRES))==10

def test_eight_scene_bounds():
    assert len(m.NOTES)==8 and len(m.BOUNDS)==9
    assert m.BOUNDS[0]==0 and m.BOUNDS[-1]==468
    assert all(a<b for a,b in zip(m.BOUNDS,m.BOUNDS[1:]))

def test_bottom_safe_band():
    assert m.CARD_X+m.CARD_WIDTH<=900
    assert m.CARD_Y>=1420
    assert m.CARD_Y+m.CARD_HEIGHT<=1700

def test_filter_generation():
    filt=m.filter_chain()
    assert filt.count("overlay=")==8
    assert "between(n,415,467)" in filt

def test_unapproved():
    state=m.publication_state()
    assert state["publication"]=="NOT_APPROVED"
    assert state["auto_post"] is False

def test_card_dimensions():
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    if not Path(font).exists(): pytest.skip("Japanese font unavailable")
    im=m.render_card(m.NOTES[0],1,font)
    assert im.size==(830,230) and im.mode=="RGBA"
