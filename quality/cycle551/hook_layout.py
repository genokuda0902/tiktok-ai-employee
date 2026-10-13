"""Cycle551: reusable caption-safe 1080x1920 video hook geometry.
Full renderer, tests and MP4 are in the cycle551 review ZIP.
No posting or publication automation is enabled.
"""
GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
VIDEO_WIDTH, VIDEO_HEIGHT = 1080, 1920
OVERLAY_X, OVERLAY_Y = 50, 250
OVERLAY_WIDTH, OVERLAY_HEIGHT = 980, 1040
CAPTION_START_Y = 1320
SCENE1_FRAMES = 53
FPS = 30
PUBLICATION_APPROVED = False
def validate_layout():
    return (len(GENRES) == 10 and OVERLAY_X >= 0 and
            OVERLAY_X + OVERLAY_WIDTH <= VIDEO_WIDTH and
            OVERLAY_Y + OVERLAY_HEIGHT < CAPTION_START_Y and
            CAPTION_START_Y < VIDEO_HEIGHT and not PUBLICATION_APPROVED)
