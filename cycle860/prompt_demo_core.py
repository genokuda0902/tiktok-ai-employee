"""Reusable 10-genre timing and safe-zone rules for cycle860 demo cards."""
from dataclasses import dataclass

WIDTH, HEIGHT = 1080, 1920
GENRE_ACCENTS = {
    "ai_work": "#3DE3CC", "business": "#50C8FF",
    "money": "#FFCB69", "health": "#68DBAB",
    "study": "#AC95FF", "travel": "#F7AE78",
    "lifestyle": "#FF8EAC", "beauty": "#F3A9E6",
    "food": "#F7C873", "technology": "#70BFFF",
}
CARD_BOX = (104, 820, 882, 1086)
CAPTION_Y = 1160

@dataclass(frozen=True)
class Card:
    name: str
    start: float
    end: float
    label: str
    title: str
    description: str
    kind: str

CARDS = (
    Card("before", 8.52, 9.20, "BEFORE | 曖昧な指示", "「いい感じに書いて」", "相手・目的・長さがわからない", "bad"),
    Card("after", 9.20, 11.10, "AFTER | 伝わる指示", "社内向け・丁寧・150字", "目的・相手・条件を指定する", "good"),
    Card("check", 11.41, 13.97, "CHECK | 人が最終確認", "数字・名前・日付を確認", "そのまま送らず、事実を見直す", "check"),
)

def validate_cards(cards=CARDS):
    names = set()
    previous_end = -1.0
    for card in cards:
        if not 0 <= card.start < card.end <= 23.034:
            raise ValueError("invalid time")
        if card.start < previous_end - 0.001:
            raise ValueError("overlapping cards")
        if card.name in names:
            raise ValueError("duplicate card")
        names.add(card.name)
        previous_end = card.end
    return True

def safe_zone():
    left, top, right, bottom = CARD_BOX
    return 0 < left < right < WIDTH and 0 < top < bottom < CAPTION_Y - 50

def filter_graph(cards=CARDS):
    validate_cards(cards)
    pieces = []
    last = "[0:v]"
    for i, c in enumerate(cards, 1):
        fade = min(0.12, (c.end - c.start) / 4)
        pieces.append(
            f"[{i}:v]format=rgba,fade=t=in:st={c.start:.3f}:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={c.end-fade:.3f}:d={fade:.3f}:alpha=1[c{i}]"
        )
        pieces.append(f"{last}[c{i}]overlay=0:0:format=auto:shortest=1[v{i}]")
        last = f"[v{i}]"
    pieces.append(f"{last}format=yuv420p[vout]")
    return ";".join(pieces)
