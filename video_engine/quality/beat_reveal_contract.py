"""Genre-neutral two-beat image-first review contract. No publishing decisions inferred."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Sequence

@dataclass(frozen=True)
class Beat:
    scene: str
    stage: int
    start: float
    end: float
    caption: str
    image_path: str

def validate_beats(beats: Sequence[Beat], manifest: Mapping) -> dict:
    if len(beats) < 8 or len(beats) % 2:
        raise ValueError('Expected at least four complete two-beat scenes')
    if manifest.get('auto_post') is not False or manifest.get('publication') != 'NOT_APPROVED':
        raise ValueError('Fail closed: automatic posting or publication approval')
    if manifest.get('rights') != 'ORIGINAL_VECTOR_ONLY' or manifest.get('personal_data') is not False:
        raise ValueError('Unverified rights or private data')
    if tuple(manifest.get('resolution', [])) != (1080, 1920):
        raise ValueError('Wrong source resolution')
    if not manifest.get('human_review_required'):
        raise ValueError('Human approval must be mandatory')
    prev = 0.0
    for i, beat in enumerate(beats):
        if beat.stage != i % 2 or not beat.scene or not beat.caption.strip():
            raise ValueError('Invalid scene stage or caption')
        if i % 2 and beat.scene != beats[i-1].scene:
            raise ValueError('Reveal must match scene')
        if beat.start < 0 or abs(beat.start-prev) > .002 or beat.end <= beat.start:
            raise ValueError('Non-contiguous timeline')
        if not beat.image_path.endswith('.png'):
            raise ValueError('Source must be a PNG image')
        prev = beat.end
    if not 15 <= prev <= 25:
        raise ValueError('Video outside short-form range')
    if manifest.get('narration') != 'VERIFIED_JAPANESE_TTS':
        return {'technical_storyboard': 'PASS', 'japanese_narration': 'FAIL', 'publication': 'NOT_APPROVED', 'duration': prev}
    if not manifest.get('voice_provenance') or not manifest.get('voice_listening_approved'):
        raise ValueError('TTS verification and human listening are required')
    return {'technical_storyboard': 'PASS', 'japanese_narration': 'TECHNICALLY_PRESENT_REQUIRES_HUMAN_REVIEW', 'publication': 'NOT_APPROVED', 'duration': prev}
