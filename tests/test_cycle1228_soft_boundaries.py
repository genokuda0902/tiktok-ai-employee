from pathlib import Path
from unittest.mock import patch
import pytest
from src.cycle1228_soft_boundaries import render_soft_boundaries

@pytest.mark.parametrize("duration,fade", [(0.5,0.35),(5,0),(1,1)])
def test_invalid_fades(duration, fade, tmp_path):
    with pytest.raises(ValueError):
        render_soft_boundaries(tmp_path/"in.mp4", tmp_path/"out.mp4", duration, fade)

def test_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError):
        render_soft_boundaries(tmp_path/"missing.mp4", tmp_path/"out.mp4", 23)

def test_ffmpeg_invocation(tmp_path):
    source=tmp_path/"in.mp4"; source.touch()
    with patch("subprocess.run") as run:
        render_soft_boundaries(source, tmp_path/"out.mp4", 23.033333)
    args=run.call_args.args[0]
    assert "fade=t=in:st=0:d=0.35" in args
    assert "afade=t=in:st=0:d=0.35" in args
    assert args[-1].endswith("out.mp4")
