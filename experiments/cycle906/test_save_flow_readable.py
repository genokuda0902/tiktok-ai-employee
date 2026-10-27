import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pytest
import save_flow_readable as s
if not Path(s.FONT).exists():
    # CI fallback tests geometry only; Japanese glyph QA requires local Noto CJK.
    s.FONT = s.FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def test_all_ten_genres_and_all_three_stages_have_safe_readable_text():
    assert len(s.GENRES) == 10
    for genre in s.GENRES:
        for stage in range(3):
            audit = []
            image = s.draw_stage(stage, genre, audit)
            assert image.size == (1080, 1100)
            assert len(audit) >= 5
            for a in audit:
                assert a['font_px'] >= 27
                assert a['bbox'][2] <= 1000
                assert a['bbox'][3] <= 1080
            for i, a in enumerate(audit):
                for b in audit[i+1:]:
                    ax1,ay1,ax2,ay2 = a['bbox']
                    bx1,by1,bx2,by2 = b['bbox']
                    assert min(ax2,bx2) <= max(ax1,bx1) or min(ay2,by2) <= max(ay1,by1), (genre,stage,a,b)

def test_genre_data_has_no_identifying_or_publication_language():
    for values in s.GENRES.values():
        for value in values:
            assert not any(x in value for x in ('@', 'http://', 'https://', '自動投稿', '実績'))

def test_sequence_frame_limits():
    assert s.FRAMES == 87
    assert s.FPS == 30
    assert s.START_SEC == 17.4
    assert s.SAFE_RECT[3] < 1100
    assert s.render_frame(0, 'ai_work').size == (1080, 1100)
    assert s.render_frame(86, 'ai_work').size == (1080, 1100)
    with pytest.raises(ValueError):
        s.render_frame(87, 'ai_work')

def test_distinct_three_stage_content():
    imgs = [s.draw_stage(i, 'ai_work') for i in range(3)]
    assert len({im.tobytes() for im in imgs}) == 3

def test_render_frame_has_dynamic_crossfades():
    images = [s.render_frame(i, 'ai_work') for i in (0, 5, 29, 35, 58, 64)]
    assert len({im.tobytes() for im in images}) == len(images)

def test_fails_closed_for_unconfigured_genre():
    with pytest.raises(ValueError):
        s.draw_stage(0, 'unknown')
    with pytest.raises(ValueError):
        s.draw_stage(3, 'ai_work')

def test_no_real_save_action_implemented():
    code = Path(s.__file__).read_text()
    assert 'requests.post(' not in code
    assert 'upload_video' not in code
    assert 'TikTokApi' not in code
    assert 'PUBLICATION_APPROVED' not in code
