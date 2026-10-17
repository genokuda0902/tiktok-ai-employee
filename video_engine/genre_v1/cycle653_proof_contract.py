"""Fail-closed, genre-agnostic numeric-evidence and caption timeline contract.
Only synthetic test data; no posting, external upload or private assets.
"""
from dataclasses import dataclass
from typing import Sequence

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし'
)
DATA = (120, 150, 200, 180)
SCENES = (
    (0, 2.0, 'AIの合計650、本当？', 'AIの答え、根拠まで見ていますか？'),
    (2, 4.5, '元データは4つ', 'まず4か月分の数字を確認'),
    (4.5, 7, '指示は具体的に', '合計と数式、グラフを依頼'),
    (7, 9.5, '自分でも足してみる', '元データを順番に足して確認'),
    (9.5, 12, '計算式で再確認', 'SUM関数の結果も確認する'),
    (12, 15, 'グラフも数字どおり？', '棒の高さと元データを照合'),
    (15, 17.5, '根拠が一致したら完了', '手計算と数式、2つで確認'),
    (17.5, 20, '保存して試してみて', '架空データから安全に練習しよう'),
)

@dataclass(frozen=True)
class Evidence:
    values: tuple[int, ...]
    claimed_total: int
    formula_total: int

    def verified(self) -> bool:
        return bool(self.values) and all(type(v) is int and v >= 0 for v in self.values) and self.claimed_total == self.formula_total == sum(self.values)

    def stamp(self) -> str:
        return '一致を確認' if self.verified() else '未検証'

def validate_timeline(scenes: Sequence[tuple], duration: float = 20.0) -> None:
    if not scenes or scenes[0][0] != 0 or scenes[-1][1] != duration:
        raise ValueError('timeline endpoints invalid')
    for idx, (start, end, title, caption) in enumerate(scenes):
        if end <= start or end-start < 1.5 or end-start > 3.5:
            raise ValueError(f'invalid scene duration {idx}')
        if idx and start != scenes[idx-1][1]:
            raise ValueError(f'timeline gap/overlap at {idx}')
        if not (1 <= len(title) <= 22 and 1 <= len(caption) <= 28):
            raise ValueError(f'unsafe caption/title length at {idx}')

def validate_review_manifest(manifest: dict) -> None:
    required = {'publication':'NOT_APPROVED', 'posting':'MANUAL_AFTER_HUMAN_APPROVAL',
                'rights':'UNVERIFIED', 'japanese_narration':'ABSENT',
                'caption_sync':'SCENE_ONLY'}
    if any(manifest.get(k) != v for k, v in required.items()):
        raise ValueError('approval or audio state incorrectly claimed')
    if manifest.get('genres_supported') != list(GENRES):
        raise ValueError('genre list invalid')
    if manifest.get('sum') != sum(DATA):
        raise ValueError('numeric evidence mismatch')

def timestamp(t: float) -> str:
    ms = round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def srt_from_timeline(scenes=SCENES) -> str:
    validate_timeline(scenes)
    return '\n\n'.join(f'{i+1}\n{timestamp(a)} --> {timestamp(b)}\n{caption}' for i,(a,b,_,caption) in enumerate(scenes))+'\n'
