from quality.cycle250.safe_area import validate_box, validate_scene_safe_area

def test_safe_box_passes():
    assert validate_box({"x": 120, "y": 300, "w": 600, "h": 500}) == []

def test_right_action_rail_fails_closed():
    errors = validate_box({"x": 780, "y": 400, "w": 180, "h": 200})
    assert "box enters right TikTok UI rail" in errors

def test_bottom_ui_fails_closed():
    errors = validate_box({"x": 120, "y": 1500, "w": 600, "h": 180})
    assert "box enters bottom TikTok UI area" in errors

def test_invalid_dimensions_fail():
    errors = validate_box({"x": 120, "y": 300, "w": 0, "h": 100})
    assert "box dimensions must be positive" in errors

def test_scene_reports_indexed_box_error():
    errors = validate_scene_safe_area({
        "important_boxes": [
            {"x": 120, "y": 300, "w": 600, "h": 500},
            {"x": 850, "y": 300, "w": 100, "h": 100},
        ]
    })
    assert errors == ["important_box 1: box enters right TikTok UI rail"]
