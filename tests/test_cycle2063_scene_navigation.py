from cycle2063_scene_navigation import make_markers, scene_at

def test_navigation():
    frames=make_markers()
    assert len(frames)==5
    assert all(im.size==(1080,1920) for im in frames)
    assert scene_at(0,22.682)==0
    assert scene_at(10,22.682)==2
    assert scene_at(22.682,22.682)==4
