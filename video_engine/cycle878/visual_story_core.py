"""Cycle878: ten-genre safe visual-story core (offline, synthetic UI only)."""
from dataclasses import dataclass

W, H, FPS = 1080, 1920, 30
CAPTION_SAFE = (68, 1438, 1012, 1670)
MAIN_VISUAL = (55, 160, 1025, 1380)
GENRES = {
    "ai_productivity": "AI・仕事効率化",
    "beauty": "美容・身だしなみ",
    "romance_psychology": "恋愛・心理",
    "money_saving": "お金・節約",
    "sales_business": "営業・ビジネス",
    "career": "転職・キャリア",
    "health_lifestyle": "健康・生活改善",
    "trivia_science": "雑学・科学",
    "travel_food": "旅行・グルメ",
    "product_lifestyle": "商品比較・暮らし",
}

@dataclass(frozen=True)
class StoryScene:
    key: str
    headline: str
    proof_type: str
    start: float
    end: float

SCENES = (
    StoryScene("hook", "AIで仕事を早くするなら", "three-step visual hook", 0.0, 3.1),
    StoryScene("tasks", "繰り返す作業を見つける", "synthetic task list", 3.1, 5.85),
    StoryScene("example", "完成形の見本を用意", "synthetic example document", 5.85, 8.45),
    StoryScene("prompt", "目的と条件を具体的に", "synthetic NG/OK prompt comparison", 8.45, 11.35),
    StoryScene("review", "出力は自分で確認", "synthetic output QA checklist", 11.35, 14.2),
    StoryScene("revise", "修正点を一つずつ伝える", "synthetic revision diff", 14.2, 17.25),
    StoryScene("template", "使える指示を保存", "synthetic reusable prompt card", 17.25, 19.85),
    StoryScene("habit", "小さな時短を習慣に", "synthetic next-action checklist", 19.85, 691/30),
)
DEMO_FOCUS = (
    ("prompt_ok", 9.12, 11.05, (110, 825, 972, 1205)),
    ("output_check", 12.10, 13.85, (130, 620, 956, 1110)),
)

def inside(rect, outer):
    x0,y0,x1,y1=rect
    a,b,c,d=outer
    return a <= x0 < x1 <= c and b <= y0 < y1 <= d

def validate_story(scenes=SCENES, focus=DEMO_FOCUS, genre="ai_productivity"):
    if genre not in GENRES:
        raise ValueError("unknown genre")
    if len(scenes)!=8 or abs(scenes[0].start)>1e-6 or abs(scenes[-1].end-691/30)>1e-4:
        raise ValueError("expected eight complete scenes")
    for i,scene in enumerate(scenes):
        if scene.start>=scene.end or (i and abs(scenes[i-1].end-scene.start)>1e-5):
            raise ValueError("scene gap or overlap")
        if not scene.headline or not scene.proof_type:
            raise ValueError("empty visual explanation")
    for _,start,end,rect in focus:
        if not 0 <= start < end <= 691/30 or not inside(rect,MAIN_VISUAL):
            raise ValueError("focus outside safe main visual")
        if rect[3] > CAPTION_SAFE[1]:
            raise ValueError("focus overlaps caption panel")
    return True
