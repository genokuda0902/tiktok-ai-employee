"""Reusable chapter takeaways for ten vertical video genres (cycle611)."""
SCENE_STARTS = (0, 70, 136, 178, 247, 287, 352, 415, 468)
TAKEAWAYS = (
    "小さくても、立派なPC",
    "カードほどのサイズ感",
    "モニターにつないで使う",
    "接続 → 電源 → 操作",
    "LEDを光らせてみよう",
    "入力が動作につながる",
    "自分だけの作品を作る",
    "気になったら保存して試す",
)
GENRE_THEMES = {
    "AI・仕事効率化": "#39e6cc",
    "美容・身だしなみ": "#e9b6cb",
    "恋愛・心理": "#f0a2a2",
    "お金・節約": "#d6dd80",
    "営業・ビジネス": "#5bcce0",
    "転職・キャリア": "#c0b1ff",
    "健康・生活改善": "#8bd1a8",
    "雑学・科学": "#55ebc8",
    "旅行・グルメ": "#f2c88d",
    "商品比較・暮らし": "#94c6f7",
}
X, Y, CARD_W, CARD_H = 80, 1490, 718, 180
PUBLICATION = "NOT_APPROVED"

def scene_for_frame(frame):
    if not 0 <= frame < SCENE_STARTS[-1]:
        raise ValueError("frame outside timeline")
    return next(i for i in range(8) if SCENE_STARTS[i] <= frame < SCENE_STARTS[i + 1])

def card_text(frame):
    return TAKEAWAYS[scene_for_frame(frame)]
