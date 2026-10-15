"""Cycle599 shared evidence-first data contract; synthetic values only."""
GENRES = {
 "AI・仕事効率化":"月別売上", "美容・身だしなみ":"月別記録",
 "恋愛・心理":"月別回答", "お金・節約":"月別支出",
 "営業・ビジネス":"月別売上", "転職・キャリア":"月別応募",
 "健康・生活改善":"月別記録", "雑学・科学":"月別観測",
 "旅行・グルメ":"月別予算", "商品比較・暮らし":"月別価格"
}
VALUES=(120,150,200,250)

def validate(genre, values=VALUES):
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    if len(values)!=4 or any(type(v) is not int or not 0<=v<=9999 for v in values):
        raise ValueError("four nonnegative integer values required")
    return {"values":list(values),"sum":sum(values),"formula":"=SUM(B2:B5)",
            "genre":genre,"label":GENRES[genre],
            "monthly":[{"month":i+1,"value":v} for i,v in enumerate(values)]}

def evidence_first_state(t, genre="AI・仕事効率化", values=VALUES):
    """The result and four inputs must exist even at frame zero."""
    if t < 0:
        raise ValueError("negative scene time")
    data=validate(genre, values)
    return {"inputs_visible":True,"total_visible":True,"formula_visible":True,
            "values":data["values"],"total":data["sum"],"formula":data["formula"]}
