"""Reusable, fictional-data visual chart plan for review-only short videos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    title: str
    subtitle: str
    bars: tuple[tuple[str, float], ...]
    seconds: int = 5

def validate(scenes):
    if not scenes or sum(s.seconds for s in scenes) > 60:
        raise ValueError("invalid duration")
    for s in scenes:
        if s.seconds <= 0 or not s.title or not s.subtitle:
            raise ValueError("invalid scene")
        if not s.bars or any(not label or value < 0 for label, value in s.bars):
            raise ValueError("invalid chart")
    return True

def sample():
    scenes = [
        Scene("残業を減らすなら", "最初に作業の見える化", (("電話",4),("入力",2),("確認",2))),
        Scene("1日の作業を3つに分ける", "架空の8時間の例", (("電話",4),("入力",2),("確認",2))),
        Scene("入力時間を半分に", "定型文とチェック表で短縮", (("従来の入力",2),("改善後",1))),
        Scene("まず1週間だけ測定", "効果が出たらチームに展開", (("従来の入力",2),("改善後",1))),
    ]
    validate(scenes)
    return scenes

PUBLICATION_NOT_APPROVED = True
FICTIONAL_DATA = True
