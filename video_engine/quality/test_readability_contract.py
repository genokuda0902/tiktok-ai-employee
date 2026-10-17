import pytest
from readability_contract import Caption, GENRES, contrast_ratio, validate_readable_captions, publication_gate

EXAMPLE = [Caption(0, 2, 'まだ手作業？', '手作業'), Caption(2, 4, 'AIで下書き', 'AI')]

@pytest.mark.parametrize('genre', GENRES)
def test_all_genres(genre):
    assert validate_readable_captions(EXAMPLE, 4, genre)

@pytest.mark.parametrize('bad', [
    [Caption(0, .7, 'まだ手作業？', '手作業'), Caption(.7, 4, 'AIで下書き', 'AI')],
    [Caption(0, 2, '一度に多くの文字を詰め込むと読めない', '文字'), Caption(2, 4, 'AIで下書き', 'AI')],
    [Caption(0, 2, 'まだ手作業？', '手作業'), Caption(2.2, 4, 'AIで下書き', 'AI')],
])
def test_reject_unreadable(bad):
    with pytest.raises(ValueError):
        validate_readable_captions(bad, 4, GENRES[0])

def test_accessible_contrast():
    assert contrast_ratio((255, 255, 255), (8, 43, 75)) >= 7
    assert contrast_ratio((102, 255, 228), (8, 43, 75)) >= 7
    assert contrast_ratio((110, 110, 110), (120, 120, 120)) < 4.5

def test_publication_fail_closed():
    assert not publication_gate({'posting_mode': 'MANUAL_ONLY'})
    assert not publication_gate({'posting_mode': 'AUTO'})
