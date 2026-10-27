import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kinetic_before_after import (
    GENRES, SCENE_TEXT, CANVAS_W, OVERLAY_H, OVERLAY_Y, FRAME_COUNT,
    phase, static_stage, render_frame
)

def test_ten_genres():
    assert len(GENRES) == 10
    assert set(GENRES) == set(SCENE_TEXT)

def test_no_fake_numeric_results_or_links():
    for lines in SCENE_TEXT.values():
        assert len(lines) == 3
        assert all(len(x) < 22 for x in lines)
        assert not any('http' in x or '@' in x for x in lines)

def test_geometry_protects_caption_band():
    assert CANVAS_W == 1080
    assert OVERLAY_Y + OVERLAY_H <= 1220

def test_phase_boundaries():
    assert [phase(i) for i in [0,28,29,57,58,86]] == [0,0,1,1,2,2]

def test_render_all_genres_and_stages():
    for genre in GENRES:
        for stage in range(3):
            img = static_stage(stage, genre)
            assert img.size == (CANVAS_W, OVERLAY_H)
            assert img.mode == 'RGBA'
            assert img.getpixel((0,0))[3] == 0
            assert img.getpixel((100,100))[3] > 0

def test_motion_and_distinct_phases():
    imgs = [render_frame(i,'ai_work') for i in [5,32,65]]
    assert imgs[0].getpixel((170,520)) != imgs[1].getpixel((170,520))
    assert imgs[1].getpixel((170,520)) != imgs[2].getpixel((170,520))

def test_bad_inputs():
    import pytest
    with pytest.raises(ValueError): phase(-1)
    with pytest.raises(ValueError): phase(87)
    with pytest.raises(ValueError): static_stage(3,'ai_work')
    with pytest.raises(ValueError): static_stage(0,'unknown')

def test_review_only_policy():
    script = (Path(__file__).resolve().parent / 'kinetic_before_after.py').read_text()
    assert 'auto_post' not in script
    assert 'publish_video' not in script
    assert 'requests.' not in script
