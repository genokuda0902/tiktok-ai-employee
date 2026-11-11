from render import SCENES
def test_storyboard():
    assert len(SCENES)==4
    assert all(a and b for a,b in SCENES)
def test_no_private_assets():
    import inspect,render
    source=inspect.getsource(render)
    assert 'IMG_5805' not in source
    assert 'REVIEW ONLY' in source
