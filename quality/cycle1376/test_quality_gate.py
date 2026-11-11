from quality_gate import publication_allowed, scene_checks

def test_reject_missing_evidence():
    assert not publication_allowed({"posting_allowed": True})

def test_reject_silent_review():
    assert not publication_allowed({"posting_allowed": False, "narration_verified": False})

def test_scene_validation():
    assert scene_checks([{"duration":2,"caption":"課題"},{"duration":2,"caption":"入力"},{"duration":2,"caption":"結果"}])
    assert not scene_checks([{"duration":2,"caption":"一場面"}])
