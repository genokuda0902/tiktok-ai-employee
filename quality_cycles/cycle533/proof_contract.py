"""Cycle533 ten-genre animated proof hook contract. REVIEW ONLY."""
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
def ease(x):
    x=max(0.,min(1.,float(x)))
    return 1-(1-x)**3
def validate(c):
    if c.get("genre") not in GENRES:raise ValueError("unknown genre")
    if c.get("rights")!="SYNTHETIC_OR_OWNER_APPROVED" or c.get("contains_private_data") is not False:raise ValueError("rights/privacy gate")
    if c.get("review_status")!="HUMAN_REVIEW" or c.get("publication")!="NOT_APPROVED":raise ValueError("publication gate")
    if c.get("claims_real_results") is not False:raise ValueError("real-results claim")
    labels,values=c.get("labels"),c.get("values")
    if not isinstance(labels,list) or len(labels)!=4 or not all(isinstance(x,str) and 1<=len(x)<=8 for x in labels):raise ValueError("four short labels required")
    if not isinstance(values,list) or len(values)!=4 or not all(type(x) is int and 0<=x<=10000 for x in values):raise ValueError("four synthetic integers required")
    if not c.get("hook") or len(c["hook"])>16:raise ValueError("hook too long")
def heights(c,t):
    validate(c)
    p=ease((t-.24)/1.08)
    scale=max(c["values"]) or 1
    return [round(315*v/scale*p) for v in c["values"]]
