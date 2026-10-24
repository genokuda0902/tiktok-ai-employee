"""cycle807 reusable Japanese caption + photographic asset quality contract.
No automatic posting, paid API calls, or rights assumptions.
The full renderer and generated local photo are in the cycle807 review ZIP.
"""
from dataclasses import dataclass
from pathlib import Path

GENRES = (
    "ai_work", "beauty", "love_psychology", "money_saving",
    "sales_business", "career", "health_life", "science",
    "travel_food", "product_life",
)
PUNCTUATION = "。、）)]"
STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"

@dataclass(frozen=True)
class VisualContract:
    genre: str
    width: int = 1080
    height: int = 1920
    fps: int = 30
    photo_rights_review_required: bool = True
    voice_license_review_required: bool = True
    employee_approval: bool = False
    auto_post: bool = False

    def validate(self):
        if self.genre not in GENRES or len(GENRES) != 10:
            raise ValueError("10-genre contract broken")
        if (self.width, self.height, self.fps) != (1080, 1920, 30):
            raise ValueError("incorrect TikTok format")
        if not self.photo_rights_review_required or not self.voice_license_review_required:
            raise ValueError("rights gate must remain enabled")
        if self.employee_approval or self.auto_post:
            raise ValueError("posting prohibited without manual approval")
        return True

def japanese_lines(text, measure, max_width, max_lines=2):
    """Split captions by glyph width, without orphaned Japanese punctuation."""
    if not text or not text.strip():
        raise ValueError("empty caption")
    if measure(text) <= max_width:
        return [text]
    candidates = [
        k for k in range(1, len(text))
        if text[k] not in PUNCTUATION and text[k - 1] not in "（("
    ]
    candidates.sort(key=lambda k: (
        0 if text[k - 1] == "、" and abs(k - len(text)/2) < 5 else 1,
        abs(k - len(text)/2)
    ))
    for k in candidates:
        lines = [text[:k], text[k:]]
        if all(measure(s) <= max_width for s in lines):
            return lines
    raise ValueError("caption cannot fit safely; reduce font or revise copy")

def assert_approved_for_posting(contract, employee_signed_off=False, rights_cleared=False):
    contract.validate()
    if not (employee_signed_off and rights_cleared):
        raise PermissionError("human review and rights clearance required")
    return True
