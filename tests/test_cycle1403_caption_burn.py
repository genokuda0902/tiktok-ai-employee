from pathlib import Path
import tempfile
import pytest
from tools.cycle1403_caption_burn import render

def test_reject_missing_source():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        with pytest.raises(FileNotFoundError):
            render(p/"missing.mp4", p/"missing.srt", p/"out.mp4")

def test_reject_empty_caption():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        (p/"input.mp4").write_bytes(b"placeholder")
        (p/"empty.srt").write_text("no timing")
        with pytest.raises(ValueError):
            render(p/"input.mp4", p/"empty.srt", p/"out.mp4")
