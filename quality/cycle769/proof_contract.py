"""Reusable ten-genre review-only proof and safe-claim validator."""
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
VALUES=(120000,150000,200000,180000)
def verify(genre, values, status, approved, posting, claim):
    if genre not in GENRES: raise ValueError("unknown genre")
    if tuple(values)!=VALUES or sum(values)!=650000: raise ValueError("false sum")
    if status!="HUMAN_REVIEW" or approved is not False: raise ValueError("approval missing")
    if posting!="employee_manual_after_approval": raise ValueError("manual posting only")
    if claim!="synthetic_arithmetic_only": raise ValueError("unverified claim")
    return True
