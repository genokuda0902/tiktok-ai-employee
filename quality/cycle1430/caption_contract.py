"""Cross-genre caption timing and publication gate; no external dependencies."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Caption:
    start_ms: int
    end_ms: int
    text: str

def validate(captions, duration_ms):
    if not captions or duration_ms <= 0:
        raise ValueError("missing captions or invalid duration")
    previous = 0
    for caption in captions:
        if not caption.text.strip():
            raise ValueError("empty caption")
        if caption.start_ms < previous or caption.end_ms <= caption.start_ms:
            raise ValueError("overlapping or inverted caption")
        if caption.end_ms > duration_ms:
            raise ValueError("caption extends past video")
        previous = caption.end_ms
    return True

def publication_gate(*, japanese_narration_verified, speech_sync_verified,
                     asset_rights_approved, employee_approved):
    return all((japanese_narration_verified, speech_sync_verified,
                asset_rights_approved, employee_approved))
