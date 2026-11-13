from qa_gate import Evidence, assess

def test_effects_do_not_count_as_narration():
    e=Evidence(True,1080,1920,False,False,True,False)
    assert not assess(e)["posting_allowed"]
    assert "narration_missing" in assess(e)["issues"]

def test_resolution_is_strict():
    e=Evidence(True,512,910,True,True,True,True)
    assert "resolution_mismatch" in assess(e)["issues"]

def test_only_fully_approved_passes():
    e=Evidence(True,1080,1920,True,True,True,True)
    assert assess(e)["posting_allowed"]
