"""Reusable phrase-level Japanese caption/audio timing gates for 10 TikTok genres.
No voice synthesis or posting; never infer native-Japanese speech from a nonzero waveform.
"""
from dataclasses import dataclass
from typing import Sequence

GENRES = ("ai_workflow", "business", "sales", "beauty", "money",
          "psychology", "career", "science", "travel", "comparison")

@dataclass(frozen=True)
class Phrase:
    text: str
    subtitle_start_s: float
    subtitle_end_s: float
    speech_start_s: float
    speech_end_s: float

def timeline(captions: Sequence[str], scene_index: int, scene_seconds: float = 3.2,
             speech_delay: float = 0.15, speech_durations: Sequence[float] | None = None) -> list[Phrase]:
    if not captions or not all(isinstance(s, str) and s.strip() for s in captions):
        raise ValueError("non-empty Japanese captions required")
    if scene_index < 0 or scene_seconds <= 0:
        raise ValueError("invalid scene")
    step = scene_seconds / len(captions)
    durations = speech_durations if speech_durations is not None else [step - speech_delay] * len(captions)
    if len(durations) != len(captions):
        raise ValueError("speech/caption count mismatch")
    out = []
    for i, (caption, duration) in enumerate(zip(captions, durations)):
        start = scene_index * scene_seconds + i * step
        if duration <= 0 or speech_delay + duration > step + 1e-6:
            raise ValueError("speech overlaps next caption")
        out.append(Phrase(caption, round(start, 4), round(start + step, 4),
                          round(start + speech_delay, 4),
                          round(start + speech_delay + duration, 4)))
    return out

def publication_gate(*, native_japanese_verified: bool, full_decode_pass: bool,
                     rights_approved: bool, employee_approved: bool) -> bool:
    """All gates are fail-closed; this does not post anything."""
    return all((native_japanese_verified, full_decode_pass, rights_approved, employee_approved))
