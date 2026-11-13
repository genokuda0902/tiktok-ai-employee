from qa import assess

def test_silent_aac_rejected():
    r=assess(dict(width=1080,height=1920,full_decode=True,audio_codec="aac",japanese_speech_verified=False,speech_caption_sync_verified=False,rights_approved=True,employee_approved=False))
    assert not r["publication_approved"]
    assert "narration" in r["failures"]

def test_resolution_rejected():
    assert "resolution" in assess(dict(width=512,height=910))["failures"]
