"""Cycle559 ten-genre reusable slide layout. Zero paid dependencies."""
GENRES={
    "ai_productivity":("AI仕事術","#2dd4bf"),
    "gadgets":("ガジェット","#2dd4bf"),
    "money_basics":("お金の基礎","#f9c66d"),
    "career":("キャリア","#81a8ff"),
    "sales":("営業","#ff9370"),
    "management":("マネジメント","#c6a2ff"),
    "psychology":("心理学","#ff92c0"),
    "health_basics":("健康の基礎","#8bdc98"),
    "daily_tips":("暮らしの工夫","#79d1ef"),
    "science":("科学","#e8ba69"),
}
SAFE_ZONES={"top":70,"left":60,"right":60,"subtitle_y_start":1130,"bottom_ui_reserved":320}
HOOK_DURATION_SECONDS=1.8

def validate():
    assert len(GENRES)==10 and len(set(GENRES))==10
    assert all(v[0] and v[1].startswith("#") and len(v[1])==7 for v in GENRES.values())
    assert SAFE_ZONES["subtitle_y_start"]>=1100
    return True
