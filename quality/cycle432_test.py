from src.quality.cycle432_story_gate import BEAT_FRAMES

def test_four_beats():
    assert len(BEAT_FRAMES) == 4
    assert sum(BEAT_FRAMES) * 8 == 600
