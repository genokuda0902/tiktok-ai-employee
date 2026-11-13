from review_quality_gate import validate
def test_silent_video_fails_closed():
    m=dict(width=1080,height=1920,video_decodes=True,japanese_narration_verified=False,captions_synchronized=False,assets_approved=True,employee_approved=False)
    result=validate(m)
    assert not result["posting_allowed"]
    assert "narration" in result["failures"]
def test_all_gates_required():
    m=dict(width=1080,height=1920,video_decodes=True,japanese_narration_verified=True,captions_synchronized=True,assets_approved=True,employee_approved=True)
    assert validate(m)["posting_allowed"]
    m["width"]=512
    assert "resolution" in validate(m)["failures"]
