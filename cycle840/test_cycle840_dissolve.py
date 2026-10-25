import pytest
from cycle840_dissolve import GENRES,PHOTO_RECT,REQUIRED,boundaries,check_policy,filter_graph

def test_trim_aware_boundaries():
    assert boundaries()==(89,170,249,336,422,511,588)

def test_seven_transitions():
    assert len(boundaries())==7
    assert all(b>a for a,b in zip(boundaries(),boundaries()[1:]))

def test_ten_genres():
    assert len(GENRES)==10
    for genre in GENRES:
        assert check_policy(dict(REQUIRED),genre)==boundaries()

def test_fail_closed():
    with pytest.raises(ValueError):check_policy({},'ai_work')
    with pytest.raises(ValueError):check_policy({**REQUIRED,'publication_approved':True},'ai_work')
    with pytest.raises(ValueError):check_policy(dict(REQUIRED),'other')

def test_dissolve_limits():
    with pytest.raises(ValueError):check_policy(dict(REQUIRED),'ai_work',0)
    with pytest.raises(ValueError):check_policy(dict(REQUIRED),'ai_work',13)

def test_photo_only_overlay():
    assert PHOTO_RECT==(62,390,1018,1390)
    graph=filter_graph(boundaries())
    assert graph.count('overlay=62:390:')==7
    assert graph.count('fade=t=out')==7
    assert '1395' not in graph
