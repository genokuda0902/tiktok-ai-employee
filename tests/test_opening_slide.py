import pytest
from tiktok_quality.opening_slide import render_intro

def test_reject_empty(tmp_path):
    with pytest.raises(ValueError):
        render_intro(tmp_path/"intro.png","","subtitle","font.ttf")

def test_reject_empty_subline(tmp_path):
    with pytest.raises(ValueError):
        render_intro(tmp_path/"intro.png","headline","","font.ttf")
