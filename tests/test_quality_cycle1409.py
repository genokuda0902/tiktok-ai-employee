from quality_cycle1409 import publication_ready

def test_silent_video_fails():
    assert not publication_ready({"video_decodes": True, "japanese_speech_verified": False})

def test_approved_passes():
    assert publication_ready(dict.fromkeys(("video_decodes", "japanese_speech_verified", "speech_caption_sync_verified", "assets_approved", "employee_approved"), True))

def test_missing_approval_fails():
    e = dict.fromkeys(("video_decodes", "japanese_speech_verified", "speech_caption_sync_verified", "assets_approved"), True)
    assert not publication_ready(e)
