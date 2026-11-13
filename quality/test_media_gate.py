from media_gate import inspect_streams

def test_silent_video_rejected():
    probe = {"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920}]}
    result = inspect_streams(probe, captions_synced=True, rights_approved=True, employee_approved=True)
    assert result["publication_approved"] is False
    assert "audio_missing" in result["problems"]

def test_approved_complete_video():
    probe = {"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
    result = inspect_streams(probe,japanese_voice_verified=True,captions_synced=True,rights_approved=True,employee_approved=True)
    assert result["publication_approved"] is True
