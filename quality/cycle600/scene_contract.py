"""Cycle600: genre-neutral synthetic spreadsheet proof state (no posting)."""
GENRES={
 "AI・仕事効率化":"月別売上","美容・身だしなみ":"月別記録",
 "恋愛・心理":"月別回答","お金・節約":"月別支出",
 "営業・ビジネス":"月別売上","転職・キャリア":"月別応募",
 "健康・生活改善":"月別記録","雑学・科学":"月別観測",
 "旅行・グルメ":"月別予算","商品比較・暮らし":"月別価格"
}
VALUES=(120,150,200,250)
FORMULA="=SUM(B2:B5)"
def ease(x):
    x=max(0.0,min(1.0,x))
    return x*x*(3-2*x)
def validate(genre,values=VALUES):
    if genre not in GENRES: raise ValueError("unsupported genre")
    if len(values)!=4 or any(type(v) is not int or not 0<=v<=9999 for v in values):
        raise ValueError("four nonnegative integer values required")
    return {"genre":genre,"label":GENRES[genre],"values":list(values),
            "sum":sum(values),"formula":FORMULA,
            "synthetic":True,"publication":"PUBLICATION_NOT_APPROVED"}
def scene_state(t,genre="AI・仕事効率化",values=VALUES):
    if not 0<=t<=4.0: raise ValueError("scene time outside 0..4")
    info=validate(genre,values)
    phase="select" if t<1.35 else "formula" if t<2.75 else "verify"
    selected=max(1,min(4,round(1+3*ease(t/1.35))))
    typed=FORMULA[:round(len(FORMULA)*ease((t-1.35)/1.25))] if t>=1.35 else ""
    return {**info,"phase":phase,"selected_cells":selected,"typed":typed,
            "result_visible":t>=2.75,"selected_range":"B2:B5",
            "caption":{"select":"B2:B5を選択","formula":"SUM関数を入力","verify":"合計720を検算"}[phase]}
