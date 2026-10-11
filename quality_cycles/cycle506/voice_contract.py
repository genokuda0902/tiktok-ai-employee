"""Cycle506: fail-closed quality contract shared across ten TikTok genres."""
GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
REQUIRED = {"native_japanese_voice":"HUMAN_VERIFIED","voice_caption_sync":"PASS","human_review":"APPROVED","publication":"MANUAL_POST_APPROVED","full_decode":"PASS"}
def check(qa):
    failures=[f"{k}: {qa.get(k,'MISSING')}" for k,v in REQUIRED.items() if qa.get(k)!=v]
    if qa.get("resolution")!=[1080,1920]: failures.append("resolution")
    if qa.get("personal_data")!="NONE": failures.append("privacy")
    if qa.get("rights")!="ORIGINAL_AND_CLEARED": failures.append("rights")
    return {"publishable":not failures,"failures":failures}
