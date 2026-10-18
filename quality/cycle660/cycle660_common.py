"""Reusable, no-cost caption and genre layout contract for ten TikTok niches."""
GENRES = {
    'ai_productivity': 'AI・仕事効率化',
    'beauty': '美容・身だしなみ',
    'relationships': '恋愛・心理',
    'money': 'お金・節約',
    'sales': '営業・ビジネス',
    'career': '転職・キャリア',
    'health': '健康・生活改善',
    'science': '雑学・科学',
    'travel': '旅行・グルメ',
    'shopping': '商品比較・暮らし',
}

def break_caption(text, measure, max_width):
    """Split into at most two lines; prefer Japanese clause boundaries."""
    if not text or not text.strip():
        raise ValueError('empty caption')
    if measure(text) <= max_width:
        return [text]
    options = []
    for i in range(3, len(text) - 3):
        a, b = text[:i], text[i:]
        if measure(a) > max_width or measure(b) > max_width:
            continue
        if b[0] in '。、！？.,!?' or a[-1] in '（(':
            continue
        clause_bonus = 1000 if a[-1] in '、。！？' else 0
        options.append((abs(measure(a) - measure(b)) - clause_bonus, i))
    if not options:
        raise ValueError('caption exceeds two safe lines')
    i = min(options)[1]
    return [text[:i], text[i:]]

def validate_contract(scenes, genre):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 1 <= len(scenes) <= 12:
        raise ValueError('invalid scene count')
    previous = 0.0
    for scene in scenes:
        start, end = float(scene['start']), float(scene['end'])
        if abs(start - previous) > 0.001 or end <= start:
            raise ValueError('noncontiguous scene timeline')
        if not scene.get('spoken_text'):
            raise ValueError('missing caption contract')
        previous = end
    return previous
