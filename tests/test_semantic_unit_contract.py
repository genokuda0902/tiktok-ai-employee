from video_engine.quality.semantic_unit_contract import validate_semantic_units

def valid_unit(**overrides):
    unit = {
        "claim_id": "classify",
        "start_seconds": 0.0,
        "end_seconds": 0.5,
        "visual_claim_id": "classify",
        "audio_claim_id": "classify",
        "caption_claim_id": "classify",
        "narration_text": "まず分類",
        "caption_text": "まず分類",
        "auto_post": False,
        "publication": "HUMAN_REVIEW_REQUIRED",
    }
    unit.update(overrides)
    return unit

def test_valid_contract_passes():
    ok, errors = validate_semantic_units([valid_unit()])
    assert ok
    assert errors == []

def test_channel_mismatch_fails_closed():
    ok, errors = validate_semantic_units([valid_unit(audio_claim_id="other")])
    assert not ok
    assert "unit_0_audio_claim_id_mismatch" in errors

def test_missing_narration_fails_closed():
    ok, errors = validate_semantic_units([valid_unit(narration_text="")])
    assert not ok
    assert "unit_0_narration_missing" in errors

def test_overlap_fails_closed():
    first = valid_unit()
    second = valid_unit(
        claim_id="summary",
        start_seconds=0.4,
        end_seconds=0.9,
        visual_claim_id="summary",
        audio_claim_id="summary",
        caption_claim_id="summary",
        narration_text="次に要点",
        caption_text="次に要点",
    )
    ok, errors = validate_semantic_units([first, second])
    assert not ok
    assert "unit_1_overlaps_previous" in errors

def test_auto_post_and_premature_publication_are_forbidden():
    ok, errors = validate_semantic_units([valid_unit(auto_post=True, publication="APPROVED")])
    assert not ok
    assert "auto_post_forbidden" in errors
    assert "publication_must_require_human_review" in errors
