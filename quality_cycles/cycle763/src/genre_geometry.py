GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約", "営業・ビジネス", "転職・キャリア", "健康・生活改善", "雑学・科学", "旅行・グルメ", "商品比較・暮らし")

def validate_genre(name):
    if name not in GENRES:
        raise ValueError("unknown genre")
    return True

def safe_caption(x0, y0, x1, y1):
    return 65 <= x0 < x1 <= 915 and 130 <= y0 < y1 <= 1620
