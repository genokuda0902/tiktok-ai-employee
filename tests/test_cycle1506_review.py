from src.quality.cycle1506_review import Review, review_video

def test_silent_placeholder_fails():
    r = Review(720,1280,8,"aac",False,False,True)
    assert not review_video(r)["approved_for_posting"]
    assert "japanese_narration_unverified" in review_video(r)["issues"]

def test_unapproved_assets_fail():
    r = Review(1080,1920,30,"aac",True,True,False)
    assert "assets_unapproved" in review_video(r)["issues"]

def test_approved_candidate_passes():
    r = Review(1080,1920,30,"aac",True,True,True)
    assert review_video(r)["approved_for_posting"]
