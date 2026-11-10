from render import SCENES,frame
def test_three_distinct_scenes():
    assert len(SCENES)==3 and len(set(SCENES))==3
def test_explicit_nonapproval():
    assert frame(0).size==(1080,1920)
    assert any('投稿禁止' in line for scene in SCENES for line in scene)
