"""Review-only common contract for ten genres (cycle773)."""
GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
MONTHS = {'1月':120000,'2月':150000,'3月':200000,'4月':180000}

def validate(m):
    if set(m.get('supported_genres',[])) != set(GENRES):
        raise ValueError('genre mismatch')
    if m.get('review_status') != 'HUMAN_REVIEW' or m.get('quality_approved') is not False:
        raise ValueError('review gate')
    if m.get('post_policy') != 'employee_manual_after_approval':
        raise ValueError('manual posting required')
    if m.get('media_rights') != 'unverified_review_only':
        raise ValueError('rights gate')
    if m.get('data') != MONTHS or sum(MONTHS.values()) != 650000:
        raise ValueError('invalid synthetic data')
    return True
