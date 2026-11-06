"""Cross-genre review-only scene and publication checks."""
def validate(scenes, duration, *, narration_verified=False, captions_synced=False, approved=False):
    if not scenes or scenes[0][0] != 0 or scenes[-1][1] != duration:
        raise ValueError("scene coverage incomplete")
    if any(a >= b for a, b in scenes):
        raise ValueError("invalid scene duration")
    if any(scenes[i][1] != scenes[i+1][0] for i in range(len(scenes)-1)):
        raise ValueError("scene gap or overlap")
    return {"scene_timing": True, "publication_allowed": bool(narration_verified and captions_synced and approved)}


def test_review_gate():
    result = validate([(0, 3), (3, 8), (8, 12), (12, 15)], 15)
    assert result["scene_timing"] and not result["publication_allowed"]


def test_bad_scene_rejected():
    try:
        validate([(0, 3), (4, 15)], 15)
    except ValueError:
        return
    raise AssertionError("gap not detected")
