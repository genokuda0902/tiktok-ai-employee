import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def test_fail_closed():
    import render
    assert len(render.SCENES)==3
    assert "REVIEW_ONLY" in Path(render.__file__).read_text()
def test_original_formula():
    import render
    assert any("SUM(B2:B4)" in x[1] for x in render.SCENES)
def test_no_auto_publish():
    import render
    source=Path(render.__file__).read_text()
    assert "tiktok upload" not in source.lower()
    assert '"publication_approved":False' in source
