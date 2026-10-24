"""Review-only visual contract for cycle809. No publication functions."""
WIDTH=1080
HEIGHT=1920
FPS=30
GENRES=("ai_work","beauty","love_psychology","money_saving","sales_business","career","health_life","science","travel_food","product_life")
PALETTES={
"ai_work":"#56AFFF","beauty":"#FF8BB7","love_psychology":"#CA8AFF","money_saving":"#78D9A8","sales_business":"#45DCC7","career":"#6DB4FF","health_life":"#9AE27A","science":"#6AD8FF","travel_food":"#FFBB73","product_life":"#A3A3FF"}
CAPTIONS=(
"仕事ができる人は、質問が違う。",
"まず、目指すゴールを確認する。",
"次に、今の数字を確かめる。",
"そして、理想との差を一つに絞る。",
"原因には、なぜを三回重ねる。",
"対策は、今日できる行動に変える。",
"結果を見て、また修正する。",
"小さな改善が、強いチームをつくる。",
)
SAFE_AREA={"left":65,"right":65,"top":110,"bottom":130}
REVIEW_STATUS="HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
AUTO_POST=False
EMPLOYEE_APPROVAL=False
PAID_SERVICES=False
def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    return PALETTES[genre]
def caption_valid(s):
    return bool(s) and len(s)<=36 and s[-1] in "。！？" and all(c not in "\n\r" for c in s)
def review_gate(approved=False):
    # This is a review-only renderer; posting must remain external and manual.
    return False
