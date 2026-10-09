from voice_gate import NARRATION, DURATIONS


def test_scene_count():
    assert len(NARRATION) == len(DURATIONS) == 7


def test_timing():
    assert abs(sum(DURATIONS) - 20.0) < 0.001


def test_nonempty_lines():
    assert all(len(line) > 5 for line in NARRATION)
