"""Cross-genre evidence integrity checks for review-only comparison scenes."""
GENRE_IDS = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)

def verify_comparison(genre, before, after, claim, status, post_policy, quality_approved):
    if genre not in GENRE_IDS:
        raise ValueError('unknown genre')
    if any(type(v) is not int or v < 0 for v in (before, after)):
        raise ValueError('values must be nonnegative integers')
    if claim != 'month_to_month_difference_only':
        raise ValueError('unverified before-after claim')
    if status != 'HUMAN_REVIEW' or quality_approved is not False:
        raise ValueError('human review required')
    if post_policy != 'employee_manual_after_approval':
        raise ValueError('automatic posting prohibited')
    return {'before': before, 'after': after, 'delta': after - before,
            'comparison_kind': 'month_to_month', 'publish_approved': False}
