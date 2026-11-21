from pathlib import Path
import pytest
from render import render

def test_missing_input_fails_closed(tmp_path):
    with pytest.raises(FileNotFoundError): render(tmp_path/'missing.mp4',tmp_path/'out.mp4')

def test_no_publication_claim():
    s=Path(__file__).with_name('render.py').read_text()
    assert "'-an'" in s
    assert 'scale=1080:1920' in s
