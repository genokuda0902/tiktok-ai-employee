"""Review-only caption timeline validation for all genres. No speech-alignment claim."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str

def validate_captions(segments, duration, *, speech_aligned=False):
    if speech_aligned:
        raise ValueError("Speech alignment requires verified narration timings")
    previous_end = 0.0
    for segment in segments:
        if not isinstance(segment.text, str) or not segment.text.strip():
            raise ValueError("Empty caption")
        if not (0 <= previous_end <= segment.start < segment.end <= duration):
            raise ValueError("Overlapping or out-of-range captions")
        previous_end = segment.end
    return {"caption_timeline_valid": True, "speech_aligned": False, "publication_approved": False}
