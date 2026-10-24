"""Cycle808 reusable 10-genre, Japanese caption and manual review contract.
No network calls, external paid services, automatic merge, or posting.
The complete local renderer, image slides and human-review MP4 are delivered
separately with their SHA256 QA manifest.
"""
from dataclasses import dataclass

GENRES = (
    "ai_work", "beauty", "love_psychology", "money_saving",
    "sales_business", "career", "health_life", "science",
    "travel_food", "product_life",
)
WIDTH, HEIGHT, FPS = 1080, 1920, 30
STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
SCENE_COUNT = 8
SENTENCES = (
    "仕事ができる人は、質問が違う。",
    "まず、目指すゴールを確認する。",
    "次に、今の数字を確かめる。",
    "そして、理想との差を一つに絞る。",
    "原因には、なぜを三回重ねる。",
    "対策は、今日できる行動に変える。",
    "結果を見て、また修正する。",
    "小さな改善が、強いチームをつくる。",
)

@dataclass(frozen=True)
class RenderContract:
    genre: str
    width: int = WIDTH
    height: int = HEIGHT
    fps: int = FPS
    scenes: int = SCENE_COUNT
    original_visuals: bool = True
    inherited_voice_license_review: bool = True
    employee_approved: bool = False
    auto_post: bool = False

    def validate(self):
        if self.genre not in GENRES or len(set(GENRES)) != 10:
            raise ValueError("invalid genre")
        if (self.width, self.height, self.fps, self.scenes) != (1080, 1920, 30, 8):
            raise ValueError("incorrect video format")
        if not self.original_visuals or not self.inherited_voice_license_review:
            raise ValueError("asset review gate missing")
        if self.employee_approved or self.auto_post:
            raise ValueError("unapproved publication")
        return True

def wrap_japanese(text, measure, width, max_lines=2):
    if not text or not text.strip():
        raise ValueError("empty caption")
    if measure(text) <= width:
        return [text]
    positions = sorted(
        (i for i in range(1, len(text))
         if text[i] not in "。、）)]" and text[i-1] not in "（("),
        key=lambda i: abs(i - len(text)/2),
    )
    for i in positions:
        parts = [text[:i], text[i:]]
        if len(parts) <= max_lines and all(measure(p) <= width for p in parts):
            return parts
    raise ValueError("caption exceeds safe area")

def allow_manual_post(contract, employee_signed_off=False, rights_cleared=False):
    contract.validate()
    if not (employee_signed_off and rights_cleared):
        raise PermissionError("manual signoff and rights clearance required")
    return True
