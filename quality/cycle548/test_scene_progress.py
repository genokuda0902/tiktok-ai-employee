SCENE_START = 165
REVEAL = 175
SCENE_END = 195

def test_timeline():
    assert SCENE_START < REVEAL <= SCENE_END
