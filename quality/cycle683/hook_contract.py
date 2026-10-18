"""Reference-inspired opening shot contract for ten genres. REVIEW ONLY."""
from dataclasses import dataclass

GENRES = ("ai_productivity", "trivia", "cooking", "beauty", "finance",
          "wellness", "travel", "product_demo", "story", "business")
SAFE_AREA = (72, 192, 1008, 1536)

@dataclass(frozen=True)
class Hook:
    genre: str
    question: str
    evidence: str
    caption_box: tuple[int, int, int, int]

def validate_hook(hook):
    if hook.genre not in GENRES:
        raise ValueError("unknown genre")
    if not hook.question.strip() or not hook.evidence.strip():
        raise ValueError("question and evidence required")
    x0, y0, x1, y1 = hook.caption_box
    a, b, c, d = SAFE_AREA
    if not (a <= x0 < x1 <= c and b <= y0 < y1 <= d):
        raise ValueError("caption outside TikTok safe area")
    return True

def allow_publication(*, japanese_voice, speech_sync, rights, human_approval):
    return all((japanese_voice, speech_sync, rights, human_approval))
