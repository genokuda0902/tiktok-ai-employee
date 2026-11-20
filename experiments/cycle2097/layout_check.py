# cycle2097: review-only slide layout and validation
# Reusable layout parameters for ten genres. No auto-posting.
SLIDE_SIZE=(1080,1920)
SCENE_SECONDS=6
SAFE_MARGIN=135
SCENES=["課題を見つける","改善を一つに絞る","仕組みに変える","結果を検証する"]
def validate_layout(size=SLIDE_SIZE, margin=SAFE_MARGIN):
    assert size==(1080,1920)
    assert 0 < margin < size[0]//4
    assert len(SCENES)==4
    return True
if __name__=="__main__":
    assert validate_layout()
