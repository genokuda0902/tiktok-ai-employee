"""Reusable, speech-independent Japanese visual-caption contract.
These are ON-SCREEN guide labels, NOT a transcript or evidence of narration.
All input data are synthetic. Review-only and publication denied by default.
"""
from dataclasses import dataclass

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし'
)
CUES = (0.0, 2.1, 4.2, 6.35, 8.4, 10.45, 12.65, 14.7)
CAPTIONS = (
    '数字4つから、グラフを作る',
    '最初に元データを確認',
    'B2:B5の範囲を選択',
    '数値を添えてAIに指示',
    'SUM関数で計算を検証',
    '120＋150＋200＋250＝720',
    'グラフと元データを比較',
    '数値の一致を確認する',
)
NARRATION_STATUS = 'ABSENT'
PUBLICATION_STATUS = 'NOT_APPROVED'

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str

def timeline(duration: float, captions=CAPTIONS, genre='AI・仕事効率化'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not 19.0 <= duration <= 30.0:
        raise ValueError('duration out of review range')
    if len(captions) != len(CUES):
        raise ValueError('caption/cue count mismatch')
    segments = tuple(Caption(CUES[i], CUES[i+1] if i+1<len(CUES) else 16.65, text)
                     for i, text in enumerate(captions))
    for seg in segments:
        if not seg.text or len(seg.text)>32 or '\n' in seg.text:
            raise ValueError('caption too long, empty, or multiline')
        if not 0 <= seg.start < seg.end <= duration:
            raise ValueError('invalid caption timing')
    return segments

def publication_gate(narration_verified=False, rights_approved=False,
                     human_approved=False, subtitle_sync_verified=False):
    return all((narration_verified, rights_approved, human_approved, subtitle_sync_verified))
