from video_engine.production_v2.caption_timeline import build_caption_timeline

GENRES = [
    "ai_work", "beauty", "psychology", "money", "sales",
    "career", "health", "science", "travel_food", "product_compare",
]

def _scenes(genre):
    return [
        {"caption": f"{genre}: 結果を先に見せる"},
        {"narration": f"{genre}: 理由を短く説明する"},
        {"caption": f"{genre}: 次の行動を示す"},
    ]

def test_all_ten_genres_share_measured_timeline_contract():
    for genre in GENRES:
        durations = [1.2, 2.1, 1.4]
        timeline = build_caption_timeline(_scenes(genre), durations)
        assert len(timeline) == 3
        assert timeline[0]["start"] == 0.0
        assert timeline[-1]["end"] == 4.7
        assert all(item["end"] > item["start"] for item in timeline)
        assert all(timeline[i]["end"] == timeline[i + 1]["start"] for i in range(2))

def test_fail_closed_on_scene_duration_outside_bounds():
    try:
        build_caption_timeline(_scenes("ai_work"), [0.2, 2.1, 1.4])
    except ValueError as exc:
        assert "outside quality bounds" in str(exc)
    else:
        raise AssertionError("expected fail-closed duration validation")

def test_fail_closed_on_total_duration_over_25_seconds():
    scenes = [{"caption": f"scene {i}"} for i in range(6)]
    try:
        build_caption_timeline(scenes, [4.5] * 6)
    except ValueError as exc:
        assert "total narration duration" in str(exc)
    else:
        raise AssertionError("expected total-duration validation")

def test_fail_closed_on_missing_caption_or_narration():
    try:
        build_caption_timeline([{"caption": ""}], [1.0])
    except ValueError as exc:
        assert "no caption/narration" in str(exc)
    else:
        raise AssertionError("expected caption validation")
