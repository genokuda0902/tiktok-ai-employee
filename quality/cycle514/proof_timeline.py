"""Reusable cycle514 review-only proof timeline; not original v33 code."""
GENRES = frozenset(("ai_work","beauty","relationship","money","sales","career","health","science","travel","products"))
BEATS = ((2.5,3.75,"pain","毎回、同じ集計作業"),(3.75,5.0,"data","まずデータを確認"),(5.0,6.25,"prompt","AIで手順を整理"),(6.25,7.5,"verify","入力→検算→結果"))
SAFE_CAPTION_Y = 1450
WIDTH, HEIGHT = 1080, 1920
def validate(m):
    if m.get("genre") not in GENRES: raise ValueError("unknown genre")
    if m.get("rights") != "synthetic_local_review_only" or m.get("privacy_checked") is not True: raise ValueError("unverified rights/privacy")
    if m.get("human_review") != "HUMAN_REVIEW" or m.get("publication") != "NOT_APPROVED" or m.get("auto_post") is not False: raise ValueError("not approved")
    v = m.get("values")
    if v != [120,150,200,250] or sum(v) != 720: raise ValueError("invalid proof")
    return m
def beat_at(t):
    return next((name for start,end,name,caption in BEATS if start <= t < end),None)
def validate_timeline():
    assert len(BEATS)==4 and BEATS[0][0]==2.5 and BEATS[-1][1]==7.5
    assert all(BEATS[i][1]==BEATS[i+1][0] for i in range(3))
    assert SAFE_CAPTION_Y==1450 and (WIDTH,HEIGHT)==(1080,1920)
    return True
