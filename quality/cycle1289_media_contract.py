"""Review-only render contract. Never treat silent videos as publication-ready."""
from dataclasses import dataclass

@dataclass(frozen=True)
class MediaQA:
    width: int
    height: int
    duration: float
    has_japanese_voice: bool
    captions_synced: bool
    assets_approved: bool
    human_approved: bool

def publication_ready(q: MediaQA) -> bool:
    return (q.width == 1080 and q.height == 1920
            and 10 <= q.duration <= 60
            and q.has_japanese_voice and q.captions_synced
            and q.assets_approved and q.human_approved)

def review_label(q: MediaQA) -> str:
    return "APPROVED" if publication_ready(q) else "REVIEW_ONLY_NOT_APPROVED"
