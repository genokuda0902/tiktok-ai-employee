"""Cycle616: reusable, rights-safe mascot hook timing and text contract.
A procedural 3D-style mascot hook can use this across ten genres.
The full PIL/ffmpeg renderer and MP4 are delivered in the review ZIP.
"""
from dataclasses import dataclass

FPS = 30
HOOK_FRAMES = 66
GENRES = (
    "ai_work", "miniature", "before_after", "science", "life_hacks",
    "finance", "food", "travel", "history", "education",
)
SAFE_Y = (120, 830)  # 540x960 working canvas; reserve platform overlays

@dataclass(frozen=True)
class HookSpec:
    genre: str = "ai_work"
    question: str = "まだ手で集計？"
    benefit: str = "数字４つからグラフへ"
    bridge: str = "その違い、見てみよう"

    def validate(self):
        if self.genre not in GENRES:
            raise ValueError("Unsupported genre")
        for text, limit in ((self.question, 12), (self.benefit, 17),
                            (self.bridge, 17)):
            if not text or len(text) > limit:
                raise ValueError("Unsafe headline length")
        return self

def phase(frame):
    if not isinstance(frame, int) or not 0 <= frame < HOOK_FRAMES:
        raise ValueError("Frame out of range")
    if frame < 25:
        return "question"
    if frame < 47:
        return "benefit"
    return "bridge"

def check_caption_box(top, bottom):
    if not 0 <= top < bottom <= 960:
        raise ValueError("Invalid bounds")
    return top >= SAFE_Y[0] and bottom <= SAFE_Y[1]
