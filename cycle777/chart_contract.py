"""Cycle777: ten-genre safe chart scene contract (review only)."""
GENRES={
"AI・仕事効率化":"#2FE4CE","美容・身だしなみ":"#FF91BE","恋愛・心理":"#F69CC7",
"お金・節約":"#EBC35E","営業・ビジネス":"#78B7FF","転職・キャリア":"#B7A1FF",
"健康・生活改善":"#78E2AA","雑学・科学":"#7BD8F0","旅行・グルメ":"#FFB77E",
"商品比較・暮らし":"#D0B1FF"}
MONTHS={"1月":120000,"2月":150000,"3月":200000,"4月":180000}
START,END,FPS=384,493,30
def validate(m):
    if len(GENRES)!=10 or set(m.get("supported_genres",()))!=set(GENRES):raise ValueError("ten genres")
    if m.get("genre") not in GENRES:raise ValueError("genre")
    if m.get("monthly_sales")!=MONTHS or m.get("total_yen")!=sum(MONTHS.values()):raise ValueError("numbers")
    if m.get("new_assets")!="original_vector_only":raise ValueError("assets")
    if m.get("source_rights")!="unverified_review_only" or m.get("audio_rights")!="unverified_review_only":raise ValueError("rights")
    if m.get("review_status")!="HUMAN_REVIEW" or m.get("quality_approved") is not False or m.get("publication_approved") is not False:raise ValueError("approval")
    if m.get("publish_mode")!="employee_manual_after_approval" or m.get("performance_claim") is not None:raise ValueError("publish/claims")
    return True
def phase(frame):
    if not START<=frame<END:raise ValueError("frame")
    t=(frame-START)/FPS
    return "paste" if t<0.50 else ("chart" if t<2.55 else "verify")
