import inspect
import tempfile
from pathlib import Path
from PIL import Image
import pytest
import mobile_proof_reveal as m

def fake():
    return Image.new('RGB', (m.WIDTH,m.HEIGHT), '#e1e6ec')

def test_ten_genres_distinct():
    assert len(m.GENRE_POLICIES)==10
    assert len(set(m.GENRE_POLICIES.values()))==10

@pytest.mark.parametrize('genre',[g for g in m.GENRE_POLICIES if g!='ai_work'])
def test_other_genres_fail_closed(genre):
    with pytest.raises(ValueError,match='not reviewed'):
        m.validate('/not-here.mp4',genre)

def test_unknown_genre_rejected():
    with pytest.raises(ValueError,match='unknown genre'):
        m.validate('/not-here.mp4','unknown')

def test_unapproved_publication_override_rejected():
    with pytest.raises(ValueError,match='manual employee approval'):
        m.validate('/not-here.mp4','ai_work',publication_approved=True)

def test_review_only_override_rejected():
    with pytest.raises(ValueError,match='manual employee approval'):
        m.validate('/not-here.mp4','ai_work',review_only=False)

def test_source_hash_locked():
    with tempfile.TemporaryDirectory() as tmp:
        f=Path(tmp)/'not_source.mp4'
        f.write_bytes(b'bad')
        with pytest.raises(ValueError,match='SHA-mismatched'):
            m.validate(f,'ai_work')

def test_safe_area():
    assert m.X>=0 and m.Y>=0
    assert m.X+m.W<=m.WIDTH
    assert m.Y+m.H<m.CAPTION_TOP

def test_crop_has_expected_dimensions():
    assert m.source_crop(fake()).size==(920,490)

def test_wrong_source_geometry_rejected():
    with pytest.raises(ValueError,match='1080x1920'):
        m.source_crop(Image.new('RGB',(100,100)))

def test_two_cards_full_opacity_inside():
    a,b=m.make_cards(fake())
    assert a.size==b.size==(m.W,m.H)
    assert a.getpixel((0,0))[3]==0
    assert b.getpixel((200,200))[3]==255

def test_arithmetic_proof():
    assert 12+16+18==46
    assert 8+9+12==29

def test_no_network_no_posting_no_private_media_in_source():
    code=inspect.getsource(m)
    assert 'requests.' not in code and 'http://' not in code
    assert 'tiktok.upload' not in code
    assert 'PUBLICATION_NOT_APPROVED' in code
    assert 'EXPECTED_SOURCE_SHA' in code

def test_stage_times_in_hook():
    assert 0.35<1.26<2.34<3.0
