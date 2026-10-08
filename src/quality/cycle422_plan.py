"""Cycle422 10-genre storyboard contract. Review-only; no publishing."""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
SCENE_SECONDS = (2.7, 2.7, 2.9, 3.3, 3.0, 2.8, 2.6)
NATIVE_JAPANESE_REQUIRED = True
PUBLICATION_APPROVED = False

def validate():
    return (len(GENRES) == len(set(GENRES)) == 10
            and len(SCENE_SECONDS) == 7
            and 15 <= sum(SCENE_SECONDS) <= 25
            and NATIVE_JAPANESE_REQUIRED
            and not PUBLICATION_APPROVED)
