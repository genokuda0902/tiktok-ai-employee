"""Reusable 10-genre Japanese CTA policy. Synthetic assets; review-only."""
PALETTES = {
 'ai_work':'#66F3E6', 'beauty':'#FFB8D4', 'love_psychology':'#FFB4E0',
 'saving':'#A6E8B4', 'sales_business':'#FFD28B', 'career':'#A8C7FF',
 'health':'#A2E5D4', 'science':'#B7B5FF', 'travel_food':'#FFBF9B',
 'product_comparison':'#C6D3FF',
}
GENRE_COPY = {
 'ai_work':'Excel集計を、あとで試そう', 'beauty':'気になる方法を保存',
 'love_psychology':'あとで振り返ろう', 'saving':'節約のヒントを保存',
 'sales_business':'営業のヒントを保存', 'career':'仕事のヒントを保存',
 'health':'健康のヒントを保存', 'science':'発見をあとで見返す',
 'travel_food':'旅のヒントを保存', 'product_comparison':'比較結果を保存',
}
CTA_TEXT = ('保存して、', 'あとで試してみて。')
PUBLICATION_APPROVED = False

def validate_genre(genre):
    if genre not in PALETTES or set(PALETTES) != set(GENRE_COPY) or len(PALETTES) != 10:
        raise ValueError('Unknown genre or incomplete configuration')
    return PALETTES[genre]
