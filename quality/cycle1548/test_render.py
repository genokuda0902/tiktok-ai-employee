from pathlib import Path
import pytest
from render import render

def test_missing_source_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        render(tmp_path / "missing.mp4", tmp_path / "out.mp4")

def test_render_real_preview(tmp_path):
    source = Path("/mnt/data/cycle1547/cycle1547_REVIEW_ONLY.mp4")
    if not source.exists():
        pytest.skip("prior synthetic source not mounted")
    out = render(source, tmp_path / "out.mp4")
    assert out.stat().st_size > 10000
