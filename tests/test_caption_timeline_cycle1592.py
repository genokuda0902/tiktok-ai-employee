from quality.caption_timeline import validate_scenes, publication_approved

def test_contiguous():
    assert validate_scenes([(0,4),(4,8),(8,12)],12)

def test_gap_rejected():
    assert not validate_scenes([(0,4),(5,12)],12)

def test_publication_gate():
    assert not publication_approved(False,True,True,False)
