from qa.cycle1362_audio_caption_gate import AudioCaptionQA, publication_allowed

def test_silent_video_blocked():
    assert not publication_allowed(AudioCaptionQA(False, False, True, False, True, True))

def test_audio_without_verified_japanese_blocked():
    assert not publication_allowed(AudioCaptionQA(True, False, True, True, True, True))

def test_unapproved_assets_blocked():
    assert not publication_allowed(AudioCaptionQA(True, True, True, True, False, True))

def test_all_gates_required():
    assert publication_allowed(AudioCaptionQA(True, True, True, True, True, True))
