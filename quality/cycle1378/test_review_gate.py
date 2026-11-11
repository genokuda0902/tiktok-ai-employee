from review_gate import review_status

def test_missing_narration_blocks():
    assert review_status({"approved_assets": True}) == "PUBLICATION_NOT_APPROVED"

def test_all_checks_only_allows_manual_review():
    m = {k: True for k in ("japanese_narration","speech_synced_captions","approved_assets","employee_approved","reproducible_renderer")}
    assert review_status(m) == "APPROVED_FOR_MANUAL_REVIEW"
