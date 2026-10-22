"""cycle775: reusable, fail-closed ten-genre chart QA contract.

No confidential media, external assets, automatic posting, or unverifiable claims.
The contract is independent of FFmpeg/Pillow and suitable for zero-cost CI.
"""
from __future__ import annotations

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)
SALES = {'1月': 120000, '2月': 150000, '3月': 200000, '4月': 180000}


def validate_contract(manifest: dict) -> bool:
    if not isinstance(manifest, dict):
        raise ValueError('manifest must be a mapping')
    if set(manifest.get('supported_genres', [])) != set(GENRES):
        raise ValueError('all ten genres are required')
    if manifest.get('genre') not in GENRES:
        raise ValueError('unknown genre')
    if manifest.get('monthly_sales') != SALES:
        raise ValueError('synthetic source data mismatch')
    if manifest.get('total_yen') != sum(SALES.values()):
        raise ValueError('wrong chart total')
    if manifest.get('asset_provenance') != 'original_vector_only':
        raise ValueError('unapproved external asset')
    if manifest.get('audio_rights') != 'unverified_review_only':
        raise ValueError('inherited audio rights cannot be assumed')
    if manifest.get('quality_approved') is not False:
        raise ValueError('quality approval required')
    if manifest.get('review_status') != 'HUMAN_REVIEW':
        raise ValueError('human review required')
    if manifest.get('publish_mode') != 'employee_manual_after_approval':
        raise ValueError('manual posting only')
    if manifest.get('time_saved_claim') is not None:
        raise ValueError('unsupported time-saving claim')
    return True


def animated_amounts(progress: float) -> tuple[int, int, int, int]:
    """Monotone source-accurate bar values for any progress in [0, 1]."""
    if not 0 <= progress <= 1:
        raise ValueError('progress outside [0,1]')
    out = []
    for i, value in enumerate(SALES.values()):
        p = min(1.0, max(0.0, (progress * 4.0 - i)))
        out.append(round(value * p))
    return tuple(out)
