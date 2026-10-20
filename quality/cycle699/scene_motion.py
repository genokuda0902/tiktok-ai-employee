"""Shared 10-genre proof animation and Japanese speech timing gates.
Source is original, synthetic, and never auto-posted.
"""
from dataclasses import dataclass

GENRES = ("AI仕事効率化","AIツール紹介","Excel活用","ビジネススキル","副業知識","デザイン","教育","科学","ガジェット","生活効率化")
ROWS = (("A101",2000),("A102",3000),("A102",3000),("A103",1000))
CAPTIONS = ("その売上、二重計上かも","4行の注文データ","A102 が重複","削除前に内容を確認","重複した1行を除外","9,000円 → 6,000円","注文ID → 重複 → 再集計","保存して次の集計に")
SPEECH = ("同じ注文が、二回。","注文を、確認。","重複を、発見。","削除前に、確認。","重複行を、除外。","合計は、六千円。","確認して、再集計。","保存して、試そう。")
@dataclass(frozen=True)
class Scene:
    index: int
    start: float
    end: float
    caption: str
    speech: str

def scenes():
    return [Scene(i,i*2.5,(i+1)*2.5,CAPTIONS[i],SPEECH[i]) for i in range(8)]

def totals():
    gross=sum(v for _,v in ROWS)
    unique=dict(ROWS)
    net=sum(unique.values())
    if gross != 9000 or net != 6000 or len(unique) != 3:
        raise ValueError("Proof values changed")
    return {"before":gross,"after":net,"removed":gross-net,"rows_before":len(ROWS),"rows_after":len(unique)}

def row_removal_progress(t):
    """0..1 visual disappearance of the duplicate row during scene 5."""
    if not 10.0 <= t <= 12.5:
        return 0.0
    return min(1.0,max(0.0,(t-10.55)/1.25))

def speech_timing(segments, duration_limit=2.35):
    if len(segments)!=8:
        raise ValueError("Eight Japanese narration segments required")
    result=[]
    for s,seconds in zip(scenes(),segments):
        if not isinstance(seconds,(int,float)) or not .2 < seconds <= duration_limit:
            raise ValueError(f"Speech timing invalid in scene {s.index}")
        result.append({"scene":s.index,"start":s.start,"end":round(s.start+seconds,3),"text":s.speech})
    return result

def review_gate(asset_approved, private_data, narration_ok, subtitle_sync_ok, employee_approved):
    if private_data or not asset_approved or not narration_ok or not subtitle_sync_ok or not employee_approved:
        return "PUBLICATION_NOT_APPROVED"
    return "READY_FOR_MANUAL_EMPLOYEE_REVIEW"
