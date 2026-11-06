from cycle1256_storyboard import SCENES, counter_value, validate_scenes, srt

def test_timeline():
    validate_scenes()
    assert len(SCENES) == 3
    assert srt().count("-->") == 3

def test_counter():
    assert counter_value(9.0) == 0
    assert counter_value(10.0) == 0
    assert counter_value(11.2) == 300
    assert counter_value(14.0) == 300
