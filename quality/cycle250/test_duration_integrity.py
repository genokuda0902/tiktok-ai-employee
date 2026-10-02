from quality.cycle250.duration_integrity import validate_duration_integrity


def plan(target=15.0, durations=None):
    durations = durations or [1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0]
    return {"target_seconds": target, "scenes": [{"seconds": v} for v in durations]}


def test_accepts_exact_duration_sum():
    assert validate_duration_integrity(plan()) == []


def test_rejects_duration_drift():
    errors = validate_duration_integrity(plan(target=15.0, durations=[2.0] * 8))
    assert errors and "does not match target" in errors[0]


def test_rejects_missing_scenes():
    assert validate_duration_integrity({"target_seconds": 15, "scenes": []}) == ["scenes required"]


def test_rejects_invalid_scene_duration():
    errors = validate_duration_integrity(plan(durations=[1.5, 2, 2, 2, 2, 2, 1.5, 0]))
    assert errors == ["all scene seconds must be positive numeric"]


def test_tolerance_boundary_is_allowed():
    durations = [1.5, 2, 2, 2, 2, 2, 1.5, 2.049]
    assert validate_duration_integrity(plan(target=15.0, durations=durations)) == []
