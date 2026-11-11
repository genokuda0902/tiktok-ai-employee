"""Cycle 1388: fail-closed timing and narration checks for all genres."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    caption: str

def validate(segments, duration, has_japanese_narration=False, approved=False):
    errors=[]
    if not segments: errors.append("missing captions")
    previous=0.0
    for s in segments:
        if not (previous <= s.start < s.end <= duration):
            errors.append("overlap/out-of-range caption")
        if not s.caption.strip(): errors.append("blank caption")
        previous=s.end
    if not has_japanese_narration: errors.append("narration unverified")
    if not approved: errors.append("employee approval missing")
    return errors

DEMO=[Segment(0,2.4,"まず4件の売上を確認"),
      Segment(2.4,4.8,"B6にカーソルを移動"),
      Segment(4.8,7.8,"B2からB5までを合計"),
      Segment(7.8,10.8,"計算結果を確認して完了")]
