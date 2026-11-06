from quality.review_guard import validate

def test_silent_blocked():
    x = validate(dict(width=720,height=1280,video_codec="h264",rights_cleared=True),approved=True)
    assert not x["publication_allowed"] and "narration" in x["errors"]

def test_employee_approval():
    x = dict(width=1080,height=1920,video_codec="h264",rights_cleared=True,japanese_narration_verified=True,captions_synchronized=True)
    assert not validate(x)["publication_allowed"]
    assert validate(x,approved=True)["publication_allowed"]
