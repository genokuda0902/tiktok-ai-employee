from cycle1286_contract import SCENES, srt, validate_publication, WIDTH, HEIGHT, POSTING_ALLOWED

def test_four_scenes():
    assert len(SCENES) == 4
    assert (WIDTH, HEIGHT) == (1080, 1920)

def test_caption_timing():
    assert "00:00:00,000 --> 00:00:03,000" in srt()
    assert "00:00:09,000 --> 00:00:12,000" in srt()

def test_fail_closed():
    assert not POSTING_ALLOWED
    assert not validate_publication()
    assert not validate_publication(audio_verified=True, captions_synced=True)
