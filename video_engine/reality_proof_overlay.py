"""Cycle151: optional evidence overlays for image-slide TikTok videos.

Keeps overlays data-driven so the same renderer can be reused across 10 genres.
Do not use claims that have not been verified by the content owner.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ProofOverlay:
    start: float
    end: float
    text: str

def ffmpeg_enable(item: ProofOverlay) -> str:
    if item.start < 0 or item.end <= item.start:
        raise ValueError("invalid overlay interval")
    if not item.text.strip():
        raise ValueError("overlay text is required")
    return f"between(t,{item.start:.2f},{item.end:.2f})"

DEFAULT_PROOF_OVERLAYS = (
    ProofOverlay(0.35, 2.45, "実測：10分 → 1分"),
    ProofOverlay(5.65, 8.10, "誇張なし・作業フローをそのまま比較"),
)
