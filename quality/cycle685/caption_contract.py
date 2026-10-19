"""Reusable 10-genre caption contract. Review-only, never publishes."""
PALETTES = {
    "ai_work": ("#40E2F2", "#91ABFF"),
    "beauty": ("#F78DD0", "#B0A1F7"),
    "love_psychology": ("#F5A7D1", "#A8CBF9"),
    "saving": ("#82E7A5", "#F3D083"),
    "sales_business": ("#57E7C0", "#F4C981"),
    "career": ("#89C3F5", "#80E1D0"),
    "health": ("#70E7B8", "#9BCDF3"),
    "science": ("#49EFD2", "#83B6FC"),
    "travel_food": ("#F3C475", "#82DCCE"),
    "product_comparison": ("#B6ABF8", "#85DBE5"),
}
CAPTIONS = {
    1: ("基板の中に、", "コンピューター。"),
    2: ("OSやアプリも", "動かせる。"),
    3: ("モニターで", "操作できる。"),
    4: ("電源と周辺機器を", "接続。"),
    5: ("光やセンサーも", "制御。"),
    6: ("入力 → 処理 →", "出力。"),
    7: ("1つ動かしてみよう。", ""),
}
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_TOP, CAPTION_BOTTOM = 1360, 1667
REVIEW_STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"

def validate(genre, scenes, approved=False, auto_post=False):
    if genre not in PALETTES:
        raise ValueError("unsupported genre")
    if scenes != list(range(1, 9)):
        raise ValueError("must have eight ordered scenes")
    if approved or auto_post:
        raise ValueError("human review and manual posting required")
    if not (0 <= CAPTION_TOP < CAPTION_BOTTOM <= HEIGHT):
        raise ValueError("caption outside frame")
    return REVIEW_STATUS
