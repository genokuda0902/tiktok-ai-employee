"""Cycle555: reusable visual hotspot configuration for 10 TikTok genres.
No paid assets, automatic publication, or human-review bypass.
The reproducible video renderer and source assets are packaged with cycle555 MP4.
"""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
VIDEO = {"width": 1080, "height": 1920, "fps": 30, "duration": 12.5}
HOTSPOT = {
    "kind": "sequential_emissive_led",
    "start": 6.60, "end": 7.53,
    "centers": [(575, 860), (718, 852), (861, 845)],
    "colors": [(255, 103, 110), (255, 218, 85), (76, 255, 224)],
    "sequence_gap": 0.22,
}
APPROVAL = {"human_review": True, "publication_approved": False, "auto_publish": False}
def validate():
    assert len(GENRES) == 10 and len(set(GENRES)) == 10
    assert VIDEO["width"] == 1080 and VIDEO["height"] == 1920
    assert 0 <= HOTSPOT["start"] < HOTSPOT["end"] < VIDEO["duration"]
    assert all(0 < x < 1080 and 0 < y < 1920 for x, y in HOTSPOT["centers"])
    assert not APPROVAL["publication_approved"] and not APPROVAL["auto_publish"]
    return True
