"""Reusable cycle500 safety contract; original synthetic scenes only."""
from dataclasses import dataclass
FRAMES=(12,12,12,12,12,15)
@dataclass(frozen=True)
class Scene:
    before:tuple[str,...]=('転記','手計算','作図')
    after:tuple[str,...]=('入力確認','SUM検算','図を照合')
    values:tuple[int,...]=(120,150,200,250)
    source:str='original_procedural'
    synthetic:bool=True
    publication_approved:bool=False
    auto_posting:bool=False
    japanese_narration_verified:bool=False

def validate(s:Scene)->int:
    if not s.synthetic or s.source!='original_procedural':
        raise ValueError('Asset provenance is not approved')
    if s.publication_approved or s.auto_posting or s.japanese_narration_verified:
        raise ValueError('Human-review-only quality gate')
    if len(s.before)!=3 or len(s.after)!=3 or len(s.values)!=4:
        raise ValueError('Comparison requires three steps and four values')
    if any(type(v)!=int or v<0 for v in s.values):
        raise ValueError('Values must be nonnegative integers')
    if any(not x or len(x)>12 for x in (*s.before,*s.after)):
        raise ValueError('Caption length')
    if sum(FRAMES)!=75:raise ValueError('2.5s scene length')
    return sum(s.values)
