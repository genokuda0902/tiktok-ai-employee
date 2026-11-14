from quality.cycle1455_gate import assess

def test_silent_video_is_rejected():
    p={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
    assert "japanese_narration_missing" in assess(p,rights_approved=True,human_approved=True,captions_verified=True)["reasons"]

def test_complete_review_passes():
    p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
    assert assess(p,rights_approved=True,human_approved=True,captions_verified=True)["publication_approved"]

def test_rights_fail_closed():
    p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
    assert not assess(p,human_approved=True,captions_verified=True)["publication_approved"]
