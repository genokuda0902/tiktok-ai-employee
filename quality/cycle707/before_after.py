"""Evidence-safe before/after overlay for 10-genre vertical videos (cycle707)."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Comparison:
    before: tuple[str, ...]
    after: tuple[str, ...]
    label: str = "工程比較のイメージ"
    evidence_for_speed: bool = False

DEFAULT = Comparison(
    before=("データを確認", "グラフを作成", "要点をまとめる"),
    after=("AIに依頼", "結果を確認", "必要なら修正"),
)
SPEED_CLAIM = re.compile(r"(\d+\s*(?:秒|分|時間)|\d+\s*[%％]|\d+倍|一瞬|必ず|確実に|劇的)")

def validate(comparison: Comparison) -> bool:
    if not (1 <= len(comparison.before) <= 4 and 1 <= len(comparison.after) <= 4):
        raise ValueError("Each comparison needs 1–4 steps")
    if any(not x.strip() or len(x) > 16 for x in comparison.before + comparison.after):
        raise ValueError("Comparison steps must be short and nonempty")
    if not comparison.evidence_for_speed and any(
        SPEED_CLAIM.search(x) for x in comparison.before + comparison.after + (comparison.label,)
    ):
        raise ValueError("Unverified speed or performance claim")
    return True

def smooth(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x*x*(3-2*x)

def draw_comparison(d, font, t: float, comparison: Comparison = DEFAULT):
    """Render into a 720x1280 authoring canvas; host d scales to native pixels."""
    validate(comparison)
    reveal = smooth((t-17.60)/0.42)
    right_reveal = smooth((t-18.18)/0.42)
    d.rounded_rectangle((53,346,669,912),radius=22,fill="#091e34",outline="#35a7db",width=3)
    d.text((90,368),"手作業 と AI支援",font=font(38),fill="#ffffff")
    d.text((91,431),"Before",font=font(27),fill="#ff9f9f")
    d.text((394,431),"After",font=font(27),fill="#7affd7")
    d.rounded_rectangle((68,479,350,823),radius=20,fill="#26364b",outline="#ed8994",width=3)
    d.rounded_rectangle((371,479,652,823),radius=20,fill="#0d4b50",outline="#34e3c0",width=3)
    for i,step in enumerate(comparison.before):
        y=515+i*95
        d.rounded_rectangle((82,y,338,y+76),radius=12,fill="#36495e")
        d.text((94,y+17),f"{i+1}. {step}",font=font(21),fill="#ffffff")
    for i,step in enumerate(comparison.after):
        y=515+i*95
        if right_reveal > i/len(comparison.after):
            d.rounded_rectangle((384,y,638,y+76),radius=12,fill="#116a67")
            d.text((397,y+17),f"{i+1}. {step}",font=font(21),fill="#ffffff")
    d.rounded_rectangle((85,844,636,891),radius=10,fill="#0b2f45")
    d.text((102,850),"工程比較の例・時間短縮効果は未検証",font=font(21),fill="#c4e4ef")
    if reveal < 1:
        d.rectangle((53,908,53+int(616*reveal),914),fill="#3fe0ca")
    return {"before_visible":True,"after_visible":right_reveal>0,"bbox":(53,346,669,914)}
