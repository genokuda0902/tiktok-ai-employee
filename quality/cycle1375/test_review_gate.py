from review_gate import evaluate

def test_review_only_fails_closed():
    assert evaluate({"approved_assets": True})["posting_allowed"] is False

def test_all_checks_required():
    manifest = dict.fromkeys(("approved_assets", "japanese_narration_verified", "captions_synced", "human_approved", "playback_verified"), True)
    assert evaluate(manifest)["posting_allowed"] is True

def test_false_is_not_accepted():
    manifest = dict.fromkeys(("approved_assets", "japanese_narration_verified", "captions_synced", "human_approved", "playback_verified"), True)
    manifest["captions_synced"] = False
    assert "captions_synced" in evaluate(manifest)["missing"]
