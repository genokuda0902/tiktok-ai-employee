"""Reusable zero-cost 10-genre video contract for cycle516."""
GENRES = {
    "ai_work": "AI・仕事効率化",
    "beauty": "美容・身だしなみ",
    "psychology": "恋愛・心理",
    "saving": "お金・節約",
    "business": "営業・ビジネス",
    "career": "転職・キャリア",
    "lifestyle": "健康・生活改善",
    "science": "雑学・科学",
    "travel": "旅行・グルメ",
    "comparison": "商品比較・暮らし",
}
WIDTH, HEIGHT, FPS = 1080, 1920, 30

def approval_gate(japanese_voice, listening_checked, caption_sync, rights_ok, employee_ok):
    return all((japanese_voice, listening_checked, caption_sync, rights_ok, employee_ok))

def validate_captions(items, maximum_cps=10.0):
    if not items:
        raise ValueError("empty captions")
    previous = 0.0
    for item in items:
        start, end, caption = item["start"], item["end"], item["caption"]
        if abs(start - previous) > 0.005:
            raise ValueError("caption gap or overlap")
        if end <= start or len(caption) / (end - start) > maximum_cps:
            raise ValueError("caption too fast")
        previous = end
    return previous

# cycle515: translation-only crop. cycle516: actual scale changes.
SEMANTIC_ZOOM = (
    "fps=30,scale=1188:2112,"
    "zoompan=z='1.015+0.045*(0.5-0.5*cos(on/16))':"
    "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
    "d=1:s=1080x1920:fps=30,format=yuv420p"
)
