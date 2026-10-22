"""Cycle776: ten-genre review-only operation demo QA."""
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
MONTHS={'1月':120000,'2月':150000,'3月':200000,'4月':180000}
def validate(m):
    if len(GENRES)!=10 or set(m['supported_genres'])!=set(GENRES): raise ValueError('genres')
    if m['genre'] not in GENRES:raise ValueError('genre')
    if m['monthly_sales']!=MONTHS or m['total_yen']!=650000:raise ValueError('numbers')
    if m['new_assets']!='original_vector_only':raise ValueError('assets')
    if m['source_rights']!='unverified_review_only' or m['audio_rights']!='unverified_review_only':raise ValueError('rights')
    if m['quality_approved'] or m['publication_approved']:raise ValueError('approval')
    if m['review_status']!='HUMAN_REVIEW' or m['publish_mode']!='employee_manual_after_approval':raise ValueError('manual')
    if m['performance_claim'] is not None:raise ValueError('claims')
    return True
def phase(frame):
    if not 195<=frame<300:raise ValueError('frame')
    t=(frame-195)/30
    return 'attach' if t<.5 else 'type' if t<2.38 else 'send' if t<2.78 else 'processing'
