"""Cross-genre, fail-closed source-evidence regression tests."""
import pytest
from pathlib import Path
from PIL import Image
from real_capture_card import synthetic_csv_evidence,crop_evidence,safe_real_capture_card

ROOT=Path(__file__).resolve().parent

def test_synthetic_csv_matches_display():
    assert synthetic_csv_evidence(ROOT/'sample_sales.csv')==(120,150,200,180)

def test_bad_source_is_rejected(tmp_path):
    p=tmp_path/'wrong.csv'
    p.write_text('月,売上（千円）\n1月,120\n2月,150\n3月,200\n4月,999\n合計,=SUM(B2:B5)\n',encoding='utf8')
    with pytest.raises(ValueError,match='inconsistent'):synthetic_csv_evidence(p)

def test_invalid_crop_rejected():
    with pytest.raises(ValueError):crop_evidence(Image.new('RGB',(10,10)),(1,1,100,100))

@pytest.mark.parametrize('mode',('table','chart'))
def test_real_capture_card_is_explicitly_not_recording(mode):
    c=Image.new('RGB',(540,960),'#08162e')
    s=Image.new('RGB',(1440,900),'white')
    m=safe_real_capture_card(c,screenshot=s,mode=mode,progress=.5)
    assert m['continuous_operation'] is False
    assert m['rights_approved'] is False
    assert c.getpixel((50,260))!=(8,22,46)

def test_unknown_screenshot_geometry_is_rejected():
    with pytest.raises(ValueError,match='Unexpected screenshot size'):
        safe_real_capture_card(Image.new('RGB',(540,960)),screenshot=Image.new('RGB',(800,600)),mode='table')

def test_missing_mode_is_rejected():
    with pytest.raises(ValueError,match='Unsupported'):
        safe_real_capture_card(Image.new('RGB',(540,960)),screenshot=Image.new('RGB',(1440,900)),mode='voice')
