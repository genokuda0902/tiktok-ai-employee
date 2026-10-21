"""Standalone zero-cost configuration and review-gate checks."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_ten_distinct_genres():
    data=json.loads((ROOT/'config/genres.json').read_text())
    assert len(data['genres'])==10
    assert len({g['name'] for g in data['genres']})==10
def test_review_gate():
    text=(ROOT/'README.md').read_text()
    assert 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED' in text
    assert 'no publishing' in text
def test_no_paid_service_config():
    data=json.loads((ROOT/'config/genres.json').read_text())
    assert all(set(g)=={'name'} for g in data['genres'])
