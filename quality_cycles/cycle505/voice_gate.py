"""Reusable 10-genre Japanese voice QA gate. Preview never means publication approval."""
from dataclasses import dataclass
from typing import Mapping

GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
          '営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学',
          '旅行・グルメ','商品比較・暮らし')

@dataclass(frozen=True)
class GateResult:
    publishable: bool
    reasons: tuple[str, ...]

def evaluate(qa: Mapping) -> GateResult:
    """Fail closed. Phonetic romanization and non-speech tracks are not native Japanese TTS."""
    required = {
        'full_decode': 'PASS',
        'native_japanese_voice': 'HUMAN_VERIFIED',
        'voice_caption_sync': 'PASS',
        'human_review': 'APPROVED',
        'publication': 'MANUAL_POST_APPROVED',
    }
    failures = tuple(f'{key}: expected {want}, got {qa.get(key, "MISSING")}'
                     for key, want in required.items() if qa.get(key) != want)
    if qa.get('resolution') != [1080, 1920]:
        failures += ('resolution: must be 1080x1920',)
    if qa.get('rights') not in ('ORIGINAL_AND_CLEARED', 'LICENSE_VERIFIED'):
        failures += ('rights: not fully cleared',)
    if qa.get('personal_data') not in ('NONE', 'REDACTED_AND_APPROVED'):
        failures += ('personal data: not cleared',)
    return GateResult(not failures, failures)
