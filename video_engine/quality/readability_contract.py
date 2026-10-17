"""Genre-independent Japanese visual-caption accessibility checks."""
from dataclasses import dataclass
from typing import Sequence

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str
    emphasis: str

def validate_readable_captions(captions: Sequence[Caption], duration: float, genre: str,
                               min_seconds: float = 1.4, max_chars_per_second: float = 8.5) -> bool:
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError('unsupported genre')
    if not captions or abs(captions[0].start) > .001 or abs(captions[-1].end - duration) > .001:
        raise ValueError('timeline endpoints invalid')
    for i, caption in enumerate(captions):
        seconds = caption.end - caption.start
        if seconds < min_seconds - 1e-6:
            raise ValueError(f'caption {i}: insufficient reading time')
        if len(caption.text) > max_chars_per_second * seconds:
            raise ValueError(f'caption {i}: too many characters per second')
        if not caption.text or caption.emphasis not in caption.text:
            raise ValueError(f'caption {i}: missing text/emphasis')
        if i and abs(captions[i-1].end - caption.start) > .001:
            raise ValueError(f'caption {i}: gap/overlap')
    return True

def contrast_ratio(rgb_a: tuple[int, int, int], rgb_b: tuple[int, int, int]) -> float:
    def luminance(rgb):
        linear = [v / 255 / 12.92 if v / 255 <= .04045 else ((v / 255 + .055) / 1.055) ** 2.4 for v in rgb]
        return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]
    a, b = sorted((luminance(rgb_a), luminance(rgb_b)), reverse=True)
    return (a + .05) / (b + .05)

def publication_gate(manifest: dict) -> bool:
    required = ('rights_approved', 'privacy_approved', 'human_approved',
                'japanese_voice_approved', 'voice_caption_sync_verified')
    return all(manifest.get(k) is True for k in required) and manifest.get('posting_mode') == 'MANUAL_ONLY'
