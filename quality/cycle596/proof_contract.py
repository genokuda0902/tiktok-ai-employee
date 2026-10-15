"""Pure validation logic for cycle596 review-only numerical proof."""
GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
VALUES = (120, 150, 200, 250)
def validate(values=VALUES, genre=GENRES[0]):
    if genre not in GENRES:
        raise ValueError("unknown genre")
    if len(values) != 4 or any(type(x) is not int or not 0 <= x <= 9999 for x in values):
        raise ValueError("invalid values")
    return sum(values)
def proof(values=VALUES, genre=GENRES[0]):
    total = validate(values, genre)
    return {"genre":genre, "values":list(values), "total":total, "formula":"=SUM(B2:B5)", "claimed_time_savings":False, "review_only":True}
