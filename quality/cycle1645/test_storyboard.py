import json
from pathlib import Path

DATA = json.loads((Path(__file__).parent / 'storyboard.json').read_text(encoding='utf-8'))

def test_duration():
    assert len(DATA['scenes']) * DATA['scene_seconds'] == DATA['duration_seconds']

def test_no_publication_without_audio_and_approval():
    assert DATA['status'] == 'PUBLICATION_NOT_APPROVED'
    assert not DATA['narration_verified']
    assert not DATA['captions_synchronized']
    assert not DATA['employee_approved']

def test_concrete_before_after():
    assert DATA['scenes'][1][0] == 'BEFORE'
    assert DATA['scenes'][2][0] == 'AFTER'
    assert DATA['scenes'][1][1] != DATA['scenes'][2][1]
