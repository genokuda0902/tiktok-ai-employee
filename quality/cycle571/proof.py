"""Cycle571: rights-aware, genre-agnostic numeric proof cards.

Reimplementation; not recovered v33. No external media. Fail closed for publication.
"""
from dataclasses import dataclass
from typing import Sequence

GENRES = (
    'AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
    '営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学',
    '旅行・グルメ','商品比較・暮らし',
)

@dataclass(frozen=True)
class Proof:
    genre: str
    heading: str
    labels: tuple[str, ...]
    values: tuple[int, ...]
    unit: str = ''
    synthetic: bool = True

    def check(self):
        if self.genre not in GENRES: raise ValueError('Unknown genre')
        if not 2 <= len(self.values) <= 6 or len(self.labels) != len(self.values):
            raise ValueError('Need 2-6 aligned values and labels')
        if any(not isinstance(x,int) or x < 0 for x in self.values):
            raise ValueError('Values must be nonnegative integers')
        if not self.synthetic: raise ValueError('Only synthetic demo inputs approved in this cycle')
        if not self.heading or not self.unit.strip() and self.genre=='お金・節約':
            raise ValueError('Heading and units required')
        return sum(self.values)


def approval_gate(status: dict):
    """Publication never follows merely from technical MP4 success."""
    if status.get('auto_post') is not False:
        raise ValueError('Auto-post prohibited')
    if status.get('publication') == 'APPROVED':
        required=('source_rights_human_verified','japanese_voice_human_verified',
                  'speech_caption_sync_human_verified','employee_approved')
        if not all(status.get(k) is True for k in required):
            raise ValueError('Missing human review gate')
    return True


def chart_bars(proof: Proof):
    """Pure semantic geometry: each bar includes its correct label and value."""
    proof.check()
    max_value=max(proof.values) or 1
    return tuple((label, value, round(value/max_value,6))
                 for label,value in zip(proof.labels,proof.values))


DEMO = Proof(genre='AI・仕事効率化',heading='架空の4か月売上',
             labels=('1月','2月','3月','4月'),values=(120,150,200,250),unit='サンプル値')
