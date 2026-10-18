"""Genre-aligned reusable signal-flow specification for TikTok image-slide videos.

The ten genres are taken from the user's initial 100-idea planning sheet.
No actual hardware measurement or outcome is claimed by these animations.
"""
from __future__ import annotations

GENRES = {
 'ai_work':('AI・仕事効率化',['指示','処理','完成'],'AI WORKFLOW'),
 'beauty':('美容・身だしなみ',['状態','手順','仕上がり'],'BEAUTY FLOW'),
 'love_psychology':('恋愛・心理',['相談','整理','言い換え'],'COMMUNICATION'),
 'saving':('お金・節約',['支出','集計','見直し'],'BUDGET FLOW'),
 'sales_business':('営業・ビジネス',['顧客','提案','次の行動'],'SALES FLOW'),
 'career':('転職・キャリア',['経験','分析','選択肢'],'CAREER FLOW'),
 'health_lifestyle':('健康・生活改善',['記録','整理','習慣'],'HABIT FLOW'),
 'science':('雑学・科学',['入力','処理','出力'],'MICRO COMPUTER'),
 'travel_food':('旅行・グルメ',['条件','比較','候補'],'TRAVEL FLOW'),
 'product_comparison':('商品比較・暮らし',['条件','比較','選択'],'PRODUCT FLOW'),
}

ACTIVATION=(.17,.86,1.56)

def stage_at(t:float)->int:
    """Return 0-based current visual stage for scene-relative seconds."""
    if t<0: raise ValueError('time must be nonnegative')
    return 0 if t<ACTIVATION[1] else (1 if t<ACTIVATION[2] else 2)

def genre_flow(genre:str):
    if genre not in GENRES: raise ValueError(f'unknown genre: {genre}')
    title,steps,context=GENRES[genre]
    assert len(steps)==3
    return {'genre':title,'steps':steps,'context':context}
