from quality_cycle496 import manifest_for
from render_cycle496 import SCENES, DATA
assert manifest_for(SCENES, DATA)['evidence_total'] == 720

def check_genres():
    return len(manifest_for(SCENES, DATA)['supported_genres']) == 10

def test_scene_frames():
    assert sum(manifest_for(SCENES, DATA)['scene_frames']) == 600

def test_genre_count():
    assert len(manifest_for(SCENES, DATA)['supported_genres']) == 10

def test_progressive_formula_frames():
    assert sum(manifest_for(SCENES, DATA)['progressive_evidence_frames']['formula']) == 75

def test_progressive_chart_frames():
    assert sum(manifest_for(SCENES, DATA)['progressive_evidence_frames']['chart']) == 75

def test_review_state():
    m=manifest_for(SCENES, DATA)
    assert m['publication'] == 'NOT_APPROVED'
    assert m['automatic_posting'] is False
    assert m['human_review'] == 'PENDING'

def test_voice_disclosure():
    m=manifest_for(SCENES, DATA)
    assert m['voice_status'] == 'SFX_ONLY_NO_JAPANESE_NARRATION'
    assert m['captions'] == 'SCENE_DESCRIPTIONS_NOT_TRANSCRIPTS'
