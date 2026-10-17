"""Cross-genre timed on-screen text contract for silent REVIEW-ONLY renders.

These are visual caption beats, NOT speech-aligned subtitles. Never set a
voice-caption-sync approval from this module.
"""
from dataclasses import dataclass
from typing import Sequence

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    text: str
    emphasis: str


def validate_beats(beats: Sequence[Beat], duration: float, genre: str) -> bool:
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('Unsupported genre')
    if not beats or abs(beats[0].start) > .001 or abs(beats[-1].end-duration) > .001:
        raise ValueError('Beats must cover complete timeline')
    for i,b in enumerate(beats):
        if not (b.start < b.end and b.end-b.start >= .45):
            raise ValueError(f'Beat too short or reversed: {i}')
        if i and abs(beats[i-1].end-b.start) > .001:
            raise ValueError(f'Gap or overlap: {i}')
        if not (1 <= len(b.text) <= 20 and b.emphasis in b.text and len(b.emphasis) <= 12):
            raise ValueError(f'Caption/emphasis invalid: {i}')
    return True


def at_time(beats: Sequence[Beat], t: float) -> Beat:
    for b in beats:
        if b.start <= t < b.end:
            return b
    if abs(t-beats[-1].end) < 1e-6:
        return beats[-1]
    raise ValueError('Time outside caption beats')


def publication_gate(manifest: dict) -> bool:
    # Caption beat timing never implies narration exists or is synchronized.
    return all(manifest.get(k) is True for k in (
        'rights_approved', 'privacy_approved', 'human_approved',
        'japanese_voice_approved', 'voice_caption_sync_verified',
    )) and manifest.get('posting_mode') == 'MANUAL_ONLY'
