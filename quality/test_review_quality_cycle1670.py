from review_quality_cycle1670 import ReviewEvidence, can_publish, shortcomings

def test_visual_motion_alone_cannot_approve():
    e = ReviewEvidence(True, False, False, True, False, False)
    assert not can_publish(e)
    assert "japanese_narration_missing" in shortcomings(e)

def test_rights_and_employee_approval_required():
    e = ReviewEvidence(True, True, True, False, False, True)
    assert not can_publish(e)

def test_complete_evidence_can_pass_contract():
    e = ReviewEvidence(True, True, True, True, True, True)
    assert can_publish(e)
