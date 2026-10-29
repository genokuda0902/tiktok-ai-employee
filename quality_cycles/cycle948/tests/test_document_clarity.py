import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from document_clarity import FocusArea, GENRE_STRENGTH, filter_complex

@pytest.mark.parametrize('genre', GENRE_STRENGTH)
def test_ten_genres_have_valid_filter(genre):
    f = filter_complex(genre)
    assert 'unsharp=5:5:' in f
    assert 'overlay=108:355' in f
    assert 'between(t,5.80,8.70)' in f
    assert 'drawtext' not in f

def test_invalid_genre():
    with pytest.raises(ValueError):
        filter_complex('unknown')

def test_subtitle_protection():
    with pytest.raises(ValueError):
        filter_complex(area=FocusArea(y=900))

def test_outside_frame():
    with pytest.raises(ValueError):
        filter_complex(area=FocusArea(x=500))

def test_invalid_time():
    with pytest.raises(ValueError):
        filter_complex(area=FocusArea(start=9, end=8))

def test_odd_crop_rejected():
    with pytest.raises(ValueError):
        filter_complex(area=FocusArea(width=827))
