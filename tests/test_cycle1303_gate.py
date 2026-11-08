from quality.cycle1303_gate import Evidence, assess

def test_audio_missing_blocks_post():
    e = Evidence(1080, 1920, True, False, True, True, True, True)
    assert not assess(e)["posting_allowed"]

def test_srt_without_speech_alignment_blocks_post():
    e = Evidence(1080, 1920, True, True, False, True, True, True)
    assert assess(e)["status"] == "REVIEW_ONLY"

def test_missing_asset_approval_blocks_post():
    e = Evidence(1080, 1920, True, True, True, False, True, True)
    assert not assess(e)["posting_allowed"]

def test_720p_blocks_post():
    e = Evidence(720, 1280, True, True, True, True, True, True)
    assert not assess(e)["posting_allowed"]
