from quality.cycle1258_gate import validate

def test_unvoiced_video_is_not_approved():
    data = dict(review_only=True, synthetic_data=True, narration="not_available",
                caption_type="scene_timed_not_speech_synced", resolution=[720, 1280])
    errors = validate(data)
    assert "Japanese narration unverified" in errors
    assert "speech-synchronized captions unverified" in errors

def test_unapproved_source_rejected():
    data = dict(review_only=True, synthetic_data=False, narration="verified_japanese",
                caption_type="speech_synced", resolution=[1080, 1920])
    assert "source approval not established" in validate(data)

def test_resolution_rejected():
    data = dict(review_only=True, synthetic_data=True, narration="verified_japanese",
                caption_type="speech_synced", resolution=[512, 910])
    assert "invalid vertical resolution" in validate(data)
