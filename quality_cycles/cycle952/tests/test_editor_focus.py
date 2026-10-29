import importlib.util
from pathlib import Path
import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("editor_focus", ROOT / "editor_focus.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

@pytest.mark.parametrize("genre", list(m.GENRE_COLORS))
def test_ten_genre_presets_have_valid_colors(genre):
    assert len(m.GENRE_COLORS[genre]) == 7
    assert m.GENRE_COLORS[genre].startswith("#")

@pytest.mark.parametrize("genre", [x for x in m.GENRE_COLORS if x != "ai_work"])
def test_unapproved_genre_geometry_fails_closed(genre):
    with pytest.raises(ValueError, match="fail closed"):
        m.validate(genre)

def test_approved_geometry():
    assert m.validate("ai_work")

@pytest.mark.parametrize("w,h,fps", [(720,1280,30),(1080,1920,24),(1920,1080,30)])
def test_wrong_video_dimensions_rejected(w,h,fps):
    with pytest.raises(ValueError):
        m.validate("ai_work",w,h,fps)

@pytest.mark.parametrize("p",m.PHASES)
def test_safe_regions(p):
    assert not any(m.intersects(p["rect"],r) for r in (m.CAPTION_ZONE,m.HEADER_ZONE,m.FOOTER_ZONE))
    assert p["start"]>=8.7 and p["end"]<=11.6

def test_three_phases_in_order():
    assert [p["label"] for p in m.PHASES]==["目的","条件","形式"]
    assert all(a["end"]<b["start"] for a,b in zip(m.PHASES,m.PHASES[1:]))

def test_overlay_is_transparent_outside_editor(tmp_path):
    path=m.render_overlay(m.PHASES[0],tmp_path/"a.png")
    im=Image.open(path)
    assert im.size==(1080,1920)
    for pt in [(100,100),(500,1300),(500,1800),(1000,800)]:
        assert im.getpixel(pt)[3]==0
    assert im.getpixel((171,700))[3]>0

def test_filter_contains_all_phases():
    fc,last=m.make_filter()
    assert last=="base3" and fc.count("overlay=")==3 and fc.count("fade=t=in")==3

def test_audio_is_stream_copied_separately():
    import inspect
    s=inspect.getsource(m.run)
    assert '"-c:a", "copy"' in s and '"-map", "1:a:0"' in s

def test_no_auto_publish_or_download():
    import inspect
    s=inspect.getsource(m)
    assert "requests." not in s and 'subprocess.run(["git"' not in s
