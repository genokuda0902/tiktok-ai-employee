def validate_scenes(scenes, duration=20):
    assert scenes[0][0] == 0
    assert scenes[-1][1] == duration
    return True
