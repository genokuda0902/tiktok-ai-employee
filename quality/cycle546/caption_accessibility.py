"""Shared zero-cost Japanese caption policy for 10 TikTok content genres.

This module contains no external assets, APIs, posting or publication logic.
"""
GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善', '雑学・科学',
    '旅行・グルメ', '商品比較・暮らし',
)
FONT_SIZE = 84
SAFE_PANEL = (72, 1280, 936, 345)  # x, y, width, height at 1080x1920
VIDEO_SIZE = (1080, 1920)
REVIEW_STATE = 'HUMAN_REVIEW'
PUBLICATION_STATE = 'NOT_APPROVED'

def validate_cues(cues, duration=12.5):
    """Return True only if ordered cues cover the entire clip without gaps."""
    if not cues or abs(cues[0][0]) > 1e-6:
        return False
    if abs(cues[-1][1] - duration) > 1e-3:
        return False
    for i, (start, end, text) in enumerate(cues):
        if end <= start or not text.strip() or len(text.replace('\\N', '')) > 20:
            return False
        if i and abs(cues[i-1][1] - start) > 1e-3:
            return False
    return True

def safe_zone_ok(panel=SAFE_PANEL, frame=VIDEO_SIZE):
    x, y, w, h = panel
    return 0 <= x < frame[0] and 0 <= y < frame[1] and x+w <= frame[0] and y+h <= frame[1]-250
