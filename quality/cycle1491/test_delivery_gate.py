from delivery_gate import publishable

def test_silent_review_rejected():
    assert not publishable({"width":720,"height":1280,"has_audio":False,"japanese_narration_verified":False,"publication_approved":False})

def test_audio_cue_not_narration():
    assert not publishable({"width":1080,"height":1920,"has_audio":True,"japanese_narration_verified":False,"publication_approved":False})
