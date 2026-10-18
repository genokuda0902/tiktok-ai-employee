"""Ten-genre Japanese narration timing contract; review-only and fail closed."""
from dataclasses import dataclass

GENRES = ("ai_productivity","trivia","cooking","beauty","finance",
          "wellness","travel","product_demo","story","business")

@dataclass(frozen=True)
class Cue:
    scene: int
    text: str
    start: float
    end: float

def make_cues(texts, durations, genre="ai_productivity"):
    if genre not in GENRES or len(texts) != 10 or len(durations) != 10:
        raise ValueError("unsupported genre or incomplete timeline")
    cues = []
    for index, (text, seconds) in enumerate(zip(texts, durations)):
        if not text.strip() or not 0.1 <= seconds <= 1.95:
            raise ValueError("missing speech or speech overflows two-second scene")
        cues.append(Cue(index, text, 2.0 * index, 2.0 * index + seconds))
    return cues

def can_publish(has_new_japanese_voice, captions_measured, assets_approved, employee_approved):
    return all((has_new_japanese_voice, captions_measured, assets_approved, employee_approved))
