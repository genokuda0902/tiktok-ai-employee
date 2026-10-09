import json
from pathlib import Path

def test_review_only():
    data = json.loads(Path(__file__).with_name('storyboard_meta.json').read_text())
    assert data['publication_status'] == 'NOT_APPROVED'
    assert data['audio_status'] == 'NOT_GENERATED'
    assert data['cost_jpy'] == 0
    assert len(data['genres']) == 10
