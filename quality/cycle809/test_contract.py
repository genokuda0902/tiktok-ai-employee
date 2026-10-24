import importlib.util
from pathlib import Path

path=Path(__file__).with_name("contract.py")
spec=importlib.util.spec_from_file_location("cycle809_contract",path)
c=importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def test_format_and_genres():
    assert (c.WIDTH,c.HEIGHT,c.FPS)==(1080,1920,30)
    assert len(c.GENRES)==len(set(c.GENRES))==10
    assert set(c.GENRES)==set(c.PALETTES)

def test_japanese_captions():
    assert len(c.CAPTIONS)==8
    assert all(c.caption_valid(x) for x in c.CAPTIONS)
    assert all(any("\u3040"<=ch<="\u9fff" for ch in x) for x in c.CAPTIONS)

def test_review_gate():
    assert not c.AUTO_POST and not c.EMPLOYEE_APPROVAL and not c.PAID_SERVICES
    assert c.review_gate(False) is False
    assert c.review_gate(True) is False
    assert c.REVIEW_STATUS=="HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"

def test_safe_margins():
    assert min(c.SAFE_AREA.values())>=60
    assert c.SAFE_AREA["bottom"]>=130

def test_genre_validation():
    for genre in c.GENRES:
        assert c.validate_genre(genre).startswith("#")
    try:
        c.validate_genre("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown genre accepted")
