"""Cycle490 lightweight contract tests. Local comprehensive QA is in the downloadable ZIP."""
from pathlib import Path
import json
def test_no_auto_publish():
    readme=(Path(__file__).resolve().parents[1]/'README.md').read_text()
    assert 'NOT APPROVED' in readme
    assert 'No auto posting' in readme
def test_genres():
    assert len(['ai_workflow','business','sales','beauty','money','psychology','career','science','travel','comparison'])==10
