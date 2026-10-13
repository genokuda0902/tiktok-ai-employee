"""Reusable zero-cost story progress overlay for ten TikTok genres (cycle547)."""
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし"
)
SCENE_START_FRAMES = (0, 53, 106, 165, 196, 230, 284, 335)
BAR_X, BAR_Y, BAR_W, BAR_H, GAP = 70, 253, 106, 11, 10
REVIEW_STATE, PUBLICATION_STATE = "HUMAN_REVIEW", "NOT_APPROVED"

def progress_filters():
    """FFmpeg drawbox chain. Keeps existing video/audio/captions untouched."""
    filters = []
    for i in range(8):
        x = BAR_X + i * (BAR_W + GAP)
        filters.append(
            f"drawbox=x={x}:y={BAR_Y}:w={BAR_W}:h={BAR_H}:color=white@0.14:t=fill"
        )
    for i, frame in enumerate(SCENE_START_FRAMES):
        x = BAR_X + i * (BAR_W + GAP)
        filters.append(
            f"drawbox=x={x}:y={BAR_Y}:w={BAR_W}:h={BAR_H}:"
            f"color=0x74FFD9@0.94:t=fill:enable='gte(n,{frame})'"
        )
    return ",".join(filters)
