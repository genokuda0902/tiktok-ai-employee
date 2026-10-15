"""Cycle603 numeric hook contract. Review only; never approves publication."""
VALUES=(120,150,200,250)
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
def validate(values=VALUES):
    if len(values)!=4 or any(type(v) is not int or v<=0 for v in values):
        raise ValueError("four positive integers required")
    if sum(values)!=720:
        raise ValueError("sum mismatch")
    return True
def publication_state():
    return "PUBLICATION_NOT_APPROVED"
