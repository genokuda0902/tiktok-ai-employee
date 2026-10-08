from scene_contract import Scene, validate

def test_scene_contract():
    assert validate([Scene(str(i), 'caption', 'voice', 2.5) for i in range(8)], rights='ORIGINAL_PROCEDURAL', publication='NOT_APPROVED')
