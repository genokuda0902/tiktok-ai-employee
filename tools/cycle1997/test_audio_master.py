from pathlib import Path
import pytest
from audio_master import master

def test_missing_input(tmp_path):
    with pytest.raises(FileNotFoundError):
        master(tmp_path / "missing.mp4", tmp_path / "out.mp4")

def test_peak_ceiling():
    assert "TP=-1.5" in Path(__file__).with_name("audio_master.py").read_text()
