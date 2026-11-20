"""Review-only timed-caption contract for 10 genre pipelines. No publication approval."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str

def validate_captions(captions, duration):
    if not captions or duration <= 0:
        raise ValueError("missing captions or duration")
    previous = 0.0
    for caption in captions:
        if abs(caption.start - previous) > 0.001:
            raise ValueError("caption gap or overlap")
        if caption.end <= caption.start or not caption.text.strip():
            raise ValueError("invalid caption")
        previous = caption.end
    if abs(previous - duration) > 0.001:
        raise ValueError("captions do not cover video")
    return True

def publication_allowed(*, japanese_speech_verified=False, speech_sync_verified=False,
                        rights_approved=False, employee_approved=False):
    return all((japanese_speech_verified, speech_sync_verified,
                rights_approved, employee_approved))
