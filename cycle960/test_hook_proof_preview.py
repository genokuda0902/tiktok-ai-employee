import tempfile
from pathlib import Path
from PIL import Image
import pytest
import hook_proof_preview as h


def fake_frame():
    im = Image.new('RGB', (h.WIDTH, h.HEIGHT), '#d5e5ea')
    return im


def test_ten_distinct_evidence_profiles():
    assert len(h.GENRE_EVIDENCE) == 10
    assert len(set(h.GENRE_EVIDENCE.values())) == 10

@pytest.mark.parametrize('genre', [g for g in h.GENRE_EVIDENCE if g != 'ai_work'])
def test_other_genres_fail_closed(genre):
    with pytest.raises(ValueError, match='not been reviewed'):
        h.validate('/nonexistent.mp4', genre)


def test_unknown_genre_fail_closed():
    with pytest.raises(ValueError, match='unknown'):
        h.validate('/nonexistent.mp4', 'gambling')


def test_publication_override_rejected():
    with pytest.raises(ValueError, match='manual employee review'):
        h.validate('/nonexistent.mp4', 'ai_work', publication_approved=True)


def test_review_flag_override_rejected():
    with pytest.raises(ValueError, match='manual employee review'):
        h.validate('/nonexistent.mp4', 'ai_work', review_only=False)


def test_missing_or_changed_source_fails_closed():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'bad.mp4'
        p.write_bytes(b'not the reviewed source')
        with pytest.raises(ValueError, match='SHA mismatch'):
            h.validate(p, 'ai_work')


def test_card_stays_above_caption():
    assert h.CARD_Y + h.CARD_H < h.CAPTION_TOP
    assert h.CARD_X + h.CARD_W < h.WIDTH


def test_card_is_transparent_outside_and_opaque_inside():
    im = h.make_card(fake_frame())
    assert im.size == (h.CARD_W, h.CARD_H)
    assert im.mode == 'RGBA'
    assert im.getpixel((0, 0))[3] == 0
    assert im.getpixel((200, 200))[3] > 240


def test_card_rejects_wrong_geometry():
    with pytest.raises(ValueError, match='1080x1920'):
        h.make_card(Image.new('RGB', (100, 100)))


def test_proof_is_from_inherited_demo_not_external_network():
    import inspect
    source = inspect.getsource(h)
    assert 'extract_frame(source, PROOF_TIME' in source
    assert 'https://' not in source
    assert 'requests.' not in source


def test_no_posting_automation():
    import inspect
    source = inspect.getsource(h)
    assert 'PUBLICATION_NOT_APPROVED' in source
    assert 'tiktok.upload' not in source
