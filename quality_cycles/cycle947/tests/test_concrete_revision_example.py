import sys
from pathlib import Path
from PIL import ImageChops
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from concrete_revision_example import (render_overlay, make_assets,
    ffmpeg_command, GENRE_ACCENTS, STAGE_TIMES, POSITION, CANVAS)

@pytest.mark.parametrize('genre', list(GENRE_ACCENTS))
def test_all_ten_genres_render(genre):
    im = render_overlay(3, genre)
    assert im.size == CANVAS
    assert im.mode == 'RGBA'
    assert im.getbbox() is not None

def test_three_progressive_stages_differ():
    a, b, c = (render_overlay(i) for i in (1, 2, 3))
    assert ImageChops.difference(a.convert('RGB'), b.convert('RGB')).getbbox() is not None
    assert ImageChops.difference(b.convert('RGB'), c.convert('RGB')).getbbox() is not None

def test_overlay_is_inside_central_panel_not_caption():
    x, y = POSITION
    assert x >= 50 and x + CANVAS[0] <= 1030
    assert y >= 970 and y + CANVAS[1] < 1390

def test_no_scene7_or_other_scene_affected():
    assert STAGE_TIMES[0][0] >= 14.5
    assert STAGE_TIMES[-1][1] <= 17.4
    assert all(a < b for a, b in STAGE_TIMES)
    assert all(STAGE_TIMES[i][1] == STAGE_TIMES[i+1][0] for i in range(2))

def test_invalid_stage_and_genre_rejected():
    with pytest.raises(ValueError): render_overlay(0)
    with pytest.raises(ValueError): render_overlay(1, 'not_a_genre')

def test_ffmpeg_keeps_audio_stream_copy(tmp_path):
    files = make_assets(tmp_path)
    cmd = ffmpeg_command(Path('input.mp4'), Path('output.mp4'), files)
    assert cmd[cmd.index('-c:a') + 1] == 'copy'
    assert '0:a:0' in cmd
    assert '-frames:v' in cmd and '691' in cmd
    assert 'gte(t,15.55)*lt(t,16.1)' in cmd[cmd.index('-filter_complex') + 1]

def test_no_external_or_publication_side_effects():
    source = (Path(__file__).resolve().parents[1] / 'concrete_revision_example.py').read_text()
    for forbidden in ('requests.', 'http://', 'https://', 'upload_video', 'post_tiktok', 'publish_video'):
        assert forbidden not in source
