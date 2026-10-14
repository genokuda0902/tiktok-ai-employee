"""Shared CTA templates for ten TikTok content genres."""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理",
    "お金・節約", "営業・ビジネス", "転職・キャリア",
    "健康・生活改善", "雑学・科学", "旅行・グルメ",
    "商品比較・暮らし",
)
FPS = 30
START_FRAME = 415
FRAME_COUNT = 53
CANVAS = (1080, 1920)
def validate():
    return len(GENRES) == 10 and START_FRAME + FRAME_COUNT == 468
