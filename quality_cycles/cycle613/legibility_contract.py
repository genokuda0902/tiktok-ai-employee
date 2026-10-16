"""Genre-neutral review-only visual proof contract for cycle613.

Source evidence is synthetic LibreOffice screen capture. No external data,
automatic publication, or voice-approval claim.
"""
from dataclasses import dataclass

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
MONTHS = ("1月", "2月", "3月", "4月")
VALUES = (120, 150, 200, 250)
WIDTH, HEIGHT, FPS = 1080, 1920, 30
START, END = 10.5, 16.5
SCENE_COUNT, BEATS_PER_SCENE, BEAT_SECONDS = 3, 5, 0.4
TEXT_SAFE_BOTTOM = 1800

@dataclass(frozen=True)
class ReviewSpec:
    genre: str = GENRES[0]
    values: tuple = VALUES
    screenshot_provenance: str = "LOCAL_LIBREOFFICE_SYNTHETIC"
    narration: str = "ABSENT"
    approval: str = "HUMAN_REVIEW"
    publication: str = "NOT_APPROVED"

    def validate(self):
        if self.genre not in GENRES:
            raise ValueError("unknown genre")
        if self.values != VALUES or sum(self.values) != 720:
            raise ValueError("numbers must match the local synthetic screenshots")
        if self.screenshot_provenance != "LOCAL_LIBREOFFICE_SYNTHETIC":
            raise ValueError("unapproved screenshot source")
        if self.narration != "ABSENT":
            raise ValueError("Japanese narration has not been generated")
        if (self.approval, self.publication) != ("HUMAN_REVIEW", "NOT_APPROVED"):
            raise ValueError("cannot publish without human approval")

def scene_at(time_seconds):
    if not START <= time_seconds < END:
        return None
    step = min(SCENE_COUNT * BEATS_PER_SCENE - 1,
               int((time_seconds - START) / BEAT_SECONDS))
    return step // BEATS_PER_SCENE, step % BEATS_PER_SCENE

def scene_data(scene, beat):
    if not (0 <= scene < SCENE_COUNT and 0 <= beat < BEATS_PER_SCENE):
        raise ValueError("invalid scene/beat")
    if scene == 0:
        return {"title": "入力値を確認", "visible": list(zip(MONTHS[:beat], VALUES[:beat]))}
    if scene == 1:
        return {"title": "SUM関数で検算", "formula": "=SUM(B2:B5)" if beat >= 1 else None,
                "calculation": sum(VALUES) if beat >= 3 else None}
    return {"title": "グラフと照合", "bars": list(zip(MONTHS[:beat], VALUES[:beat])),
            "maximum": 250 if beat == 4 else None}
